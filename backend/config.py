"""Central configuration, loaded once from environment variables / the .env file."""
import os

from dotenv import load_dotenv

load_dotenv()


def _int(name: str, default: int) -> int:
    try:
        return int(os.getenv(name, default))
    except ValueError:
        return default


def _float(name: str, default: float) -> float:
    try:
        return float(os.getenv(name, default))
    except ValueError:
        return default


# ---- Database ----
MONGO_URI = os.getenv("MONGO_URI", "").strip()  # empty = in-memory demo mode
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "careerguide")
MONGO_MAX_POOL_SIZE = _int("MONGO_MAX_POOL_SIZE", 50)
MONGO_MIN_POOL_SIZE = _int("MONGO_MIN_POOL_SIZE", 5)
MONGO_SERVER_SELECTION_TIMEOUT_MS = _int("MONGO_SERVER_SELECTION_TIMEOUT_MS", 5000)
DB_MAX_RETRIES = _int("DB_MAX_RETRIES", 5)
DB_RETRY_DELAY_SECONDS = _float("DB_RETRY_DELAY_SECONDS", 1.0)

# ---- CORS: local development + live URLs ----
_DEFAULT_ORIGINS = (
    "http://localhost:8501,http://127.0.0.1:8501,"
    "http://localhost:3000,http://127.0.0.1:3000"
)
CORS_ORIGINS = [
    o.strip().rstrip("/")
    for o in os.getenv("CORS_ORIGINS", _DEFAULT_ORIGINS).split(",")
    if o.strip()
]

# ---- LLM (optional) ----
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "").strip()
LLM_MODEL = os.getenv("LLM_MODEL", "claude-sonnet-5-5")