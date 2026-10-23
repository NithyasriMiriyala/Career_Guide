"""Email + password accounts. Passwords are stored only as salted PBKDF2-SHA256 hashes."""
import hashlib
import hmac
import os
import re
import secrets
import time

from . import database

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
ITERATIONS = 200_000
MIN_PASSWORD = 8
MAX_PASSWORD = 128
MAX_FAILS = 5
LOCK_SECONDS = 300
# collections that may already hold data saved under the old email-hash id
LEGACY_COLLECTIONS = ("profiles", "resumes", "applications", "skill_progress")


class AuthError(Exception):
    def __init__(self, status: int, message: str):
        super().__init__(message)
        self.status = status
        self.message = message


def email_key(email: str) -> str:
    """The old (guessable) id: it is now only the lookup key for the account record."""
    return hashlib.sha256(email.strip().lower().encode()).hexdigest()[:12]


def hash_password(password: str, salt_hex: str = "") -> tuple:
    salt = bytes.fromhex(salt_hex) if salt_hex else os.urandom(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, ITERATIONS)
    return salt.hex(), digest.hex()


def verify_password(password: str, salt_hex: str, hash_hex: str) -> bool:
    _, digest = hash_password(password, salt_hex)
    return hmac.compare_digest(digest, hash_hex)


def _clean_email(email: str) -> str:
    e = (email or "").strip().lower()
    if not EMAIL_RE.match(e) or len(e) > 254:
        raise AuthError(400, "Please enter a valid email address.")
    return e


def register(email: str, password: str) -> str:
    e = _clean_email(email)
    if not MIN_PASSWORD <= len(password or "") <= MAX_PASSWORD:
        raise AuthError(400, f"Password must be {MIN_PASSWORD} to {MAX_PASSWORD} characters.")
    key = email_key(e)
    if database.get_doc("users", key):
        raise AuthError(409, "An account with this email already exists. Please log in.")
    # an email used before passwords existed keeps its saved data
    legacy = any(database.get_doc(c, key) for c in LEGACY_COLLECTIONS)
    uid = key if legacy else secrets.token_hex(8)
    salt, digest = hash_password(password)
    database.save_doc("users", key, {"email": e, "uid": uid, "salt": salt, "hash": digest,
                                      "created_at": time.time(), "failed": 0, "locked_until": 0})
    return uid


def login(email: str, password: str) -> str:
    e = _clean_email(email)
    key = email_key(e)
    user = database.get_doc("users", key)
    if not user:
        hash_password(password or "")  # same work as a real check, so timing doesn't reveal accounts
        raise AuthError(401, "Wrong email or password.")
    now = time.time()
    if user.get("locked_until", 0) > now:
        minutes = int((user["locked_until"] - now) // 60) + 1
        raise AuthError(429, f"Too many wrong attempts. Try again in about {minutes} minute(s).")
    if not verify_password(password or "", user["salt"], user["hash"]):
        user["failed"] = user.get("failed", 0) + 1
        if user["failed"] >= MAX_FAILS:
            user["failed"], user["locked_until"] = 0, now + LOCK_SECONDS
        database.save_doc("users", key, user)
        raise AuthError(401, "Wrong email or password.")
    if user.get("failed") or user.get("locked_until"):
        user["failed"], user["locked_until"] = 0, 0
        database.save_doc("users", key, user)
    return user["uid"]