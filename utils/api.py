"""Small helper that talks to the FastAPI backend. Returns None when the backend is unreachable."""
import os
from datetime import date

import requests
from dotenv import load_dotenv

load_dotenv()
BASE = os.getenv("API_BASE_URL", "http://127.0.0.1:8000").rstrip("/")


def _req(method: str, path: str, **kwargs):
    try:
        r = requests.request(method, f"{BASE}{path}", timeout=60, **kwargs)
        r.raise_for_status()
        return r.json()
    except (requests.RequestException, ValueError):
        return None


def health():
    return _req("GET", "/health")


def save_profile(uid: str, profile: dict, targets: dict) -> bool:
    payload = dict(profile)
    if isinstance(payload.get("dob"), date):
        payload["dob"] = payload["dob"].isoformat()
    payload.update({"user_id": uid, "targets": targets})
    return _req("PUT", "/profiles", json=payload) is not None


def get_profile(uid: str):
    data = _req("GET", f"/profiles/{uid}")
    if not data:
        return None
    data = {k: v for k, v in data.items() if v is not None}
    if isinstance(data.get("dob"), str):
        data["dob"] = date.fromisoformat(data["dob"])
    return data


def chat(uid: str, message: str, mode: str = "career"):
    return _req("POST", "/chat", json={"user_id": uid, "message": message, "mode": mode})
def save_resume(uid: str, d: dict):
    keys = ("name", "role", "email", "phone", "location", "linkedin", "summary",
            "education", "experience", "projects", "certificates", "volunteer", "hobbies")
    payload = {k: d.get(k, "") for k in keys}
    payload.update({"user_id": uid, "skills": d.get("skills", [])})
    return _req("POST", "/resume", json=payload)