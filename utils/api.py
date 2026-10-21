"""Small helper that talks to the FastAPI backend. Returns None when the backend is unreachable."""
import os
from datetime import date

import requests
from dotenv import load_dotenv

load_dotenv()
BASE = os.getenv("API_BASE_URL", "http://127.0.0.1:8000").rstrip("/")


class ApiError(Exception):
    """Raised by the jobs / progress helpers when the backend can't be reached."""


def _req(method: str, path: str, **kwargs):
    try:
        r = requests.request(method, f"{BASE}{path}", timeout=60, **kwargs)
        r.raise_for_status()
        return r.json()
    except (requests.RequestException, ValueError):
        return None


def _strict(method: str, path: str, **kwargs):
    try:
        r = requests.request(method, f"{BASE}{path}", timeout=60, **kwargs)
        r.raise_for_status()
        return r.json()
    except (requests.RequestException, ValueError) as exc:
        raise ApiError(str(exc)) from exc


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


# ---------- Jobs and applications ----------
def get_jobs(skills: list, q: str = "", location: str = "India", page: int = 1) -> dict:
    """Real job listings (Adzuna) or search links. Returns {"source", "jobs", "note"}."""
    return _strict("GET", "/jobs", params={
        "skills": ",".join(skills), "q": q, "location": location, "page": page})


def mark_applied(uid: str, job: dict, skills: list) -> dict:
    """Record that the user applied to a job."""
    keep = {k: job.get(k, "") for k in ("id", "title", "company", "location", "url", "source")}
    return _strict("POST", "/applications", json={"user_id": uid, "job": keep, "skills": skills})


def get_applications(uid: str) -> dict:
    """{"total", "this_month", "by_skill", "by_month", "items"}"""
    return _strict("GET", f"/applications/{uid}")


# ---------- Skill progress (ticks on the Skill Gap page) ----------
def set_skill_done(uid: str, skill: str, done: bool) -> dict:
    return _strict("POST", "/skill-progress", json={"user_id": uid, "skill": skill, "done": done})


def get_skill_progress(uid: str) -> dict:
    """{"total", "completed": [skills], "by_month", "items"}"""
    return _strict("GET", f"/skill-progress/{uid}")