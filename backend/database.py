"""Database layer: MongoDB with connection pooling + retry, and an in-memory fallback."""
import functools
import logging
import threading
import time
from typing import Any, Callable, Dict, List, Optional

import certifi
from pymongo import MongoClient
from pymongo.errors import AutoReconnect, ConnectionFailure, PyMongoError

from . import config

log = logging.getLogger("careerguide.db")

_client: Optional[MongoClient] = None
_lock = threading.Lock()
_use_memory = False
_memory: Dict[str, Dict[str, Dict[str, Any]]] = {}   # collection -> user_id -> document
_chats: Dict[str, List[Dict[str, Any]]] = {}          # user_id -> messages


def retry(func: Callable) -> Callable:
    """Retry temporary connection errors a few times before giving up."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        last: Optional[Exception] = None
        for attempt in range(1, config.DB_MAX_RETRIES + 1):
            try:
                return func(*args, **kwargs)
            except (AutoReconnect, ConnectionFailure) as exc:
                last = exc
                log.warning("DB error (attempt %s/%s): %s", attempt, config.DB_MAX_RETRIES, exc)
                time.sleep(config.DB_RETRY_DELAY_SECONDS * attempt)
        raise last  # type: ignore[misc]

    return wrapper


@retry
def _connect() -> MongoClient:
    client = MongoClient(
        config.MONGO_URI,
        maxPoolSize=config.MONGO_MAX_POOL_SIZE,
        minPoolSize=config.MONGO_MIN_POOL_SIZE,
        serverSelectionTimeoutMS=config.MONGO_SERVER_SELECTION_TIMEOUT_MS,
        retryWrites=True,
        retryReads=True,
        tlsCAFile=certifi.where(),   # fixes SSL CERTIFICATE_VERIFY_FAILED on macOS
    )
    client.admin.command("ping")  # confirm the connection works at startup
    return client


def init_db() -> str:
    """Connect once at startup. Returns 'mongodb' or 'memory'."""
    global _client, _use_memory
    with _lock:
        if _client is not None:
            return "mongodb"
        if not config.MONGO_URI:
            _use_memory = True
            log.warning("MONGO_URI is empty - using the in-memory store (data is lost on restart).")
            return "memory"
        try:
            _client = _connect()
            _use_memory = False
            log.info("Connected to MongoDB.")
            return "mongodb"
        except PyMongoError as exc:
            _client, _use_memory = None, True
            log.error("MongoDB unavailable (%s) - falling back to the in-memory store.", exc)
            return "memory"


def backend_name() -> str:
    return "memory" if _use_memory or _client is None else "mongodb"


def _db():
    return _client[config.MONGO_DB_NAME]  # type: ignore[index]


@retry
def save_doc(collection: str, user_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
    """Create or replace one document per user in a collection (profiles, resumes, progress...)."""
    doc = dict(data, user_id=user_id)
    if backend_name() == "memory":
        _memory.setdefault(collection, {})[user_id] = doc
    else:
        _db()[collection].replace_one({"user_id": user_id}, doc, upsert=True)
    return doc


@retry
def get_doc(collection: str, user_id: str) -> Optional[Dict[str, Any]]:
    if backend_name() == "memory":
        d = _memory.get(collection, {}).get(user_id)
        return dict(d) if d else None
    return _db()[collection].find_one({"user_id": user_id}, {"_id": 0})


@retry
def append_chat(user_id: str, role: str, content: str) -> None:
    msg = {"user_id": user_id, "role": role, "content": content, "ts": time.time()}
    if backend_name() == "memory":
        _chats.setdefault(user_id, []).append(msg)
    else:
        _db()["chats"].insert_one(msg)


@retry
def get_chat(user_id: str, limit: int = 20) -> List[Dict[str, Any]]:
    if backend_name() == "memory":
        return list(_chats.get(user_id, []))[-limit:]
    cur = _db()["chats"].find({"user_id": user_id}, {"_id": 0}).sort("ts", -1).limit(limit)
    return list(reversed(list(cur)))


def reset_memory_store() -> None:
    """Used by tests."""
    _memory.clear()
    _chats.clear()