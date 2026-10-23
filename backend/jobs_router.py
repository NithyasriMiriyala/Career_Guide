"""Real job listings (Adzuna API, or search links as a fallback) + application tracking."""
import logging
import os
import re
import time
from collections import Counter
from datetime import datetime, timezone
from typing import Any, Dict, List, Tuple
from urllib.parse import quote_plus

import httpx
from dotenv import load_dotenv
from fastapi import APIRouter, Query
from pydantic import BaseModel, Field

from . import database

load_dotenv()
log = logging.getLogger("careerguide.jobs")
router = APIRouter(tags=["jobs"])

_CACHE: Dict[str, Tuple[float, Any]] = {}
CACHE_SECONDS = 600  # reuse results for 10 minutes to save API quota


def _slug(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def _skills_in(text: str, skills: List[str]) -> List[str]:
    low = text.lower()
    return [s for s in skills
            if re.search(r"(?<![a-z0-9+#])" + re.escape(s.lower()) + r"(?![a-z0-9+#])", low)]


def _adzuna(skills: List[str], q: str, location: str, page: int) -> List[Dict[str, Any]]:
    app_id, app_key = os.getenv("ADZUNA_APP_ID", ""), os.getenv("ADZUNA_APP_KEY", "")
    country = os.getenv("ADZUNA_COUNTRY", "in")
    params = {"app_id": app_id, "app_key": app_key, "results_per_page": 20,
            "content-type": "application/json"}
    if q:
        params["what"] = q
    if skills:
        params["what_or"] = " ".join(skills)
    if location and location.lower() not in ("india", "any"):
        params["where"] = location
    r = httpx.get(f"https://api.adzuna.com/v1/api/jobs/{country}/search/{page}",
                params=params, timeout=12)
    r.raise_for_status()
    jobs = []
    for j in r.json().get("results", []):
        text = f"{j.get('title', '')} {j.get('description', '')}"
        jobs.append({
            "id": f"adzuna-{j.get('id')}",
            "title": re.sub(r"</?strong>", "", j.get("title", "")),
            "company": (j.get("company") or {}).get("display_name", ""),
            "location": (j.get("location") or {}).get("display_name", ""),
            "url": j.get("redirect_url", ""),
            "source": "Adzuna",
            "posted": (j.get("created") or "")[:10],
            "salary_min": j.get("salary_min"),
            "salary_max": j.get("salary_max"),
            "skills_matched": _skills_in(text, skills),
            "kind": "job",
        })
    return jobs


def _search_links(skills: List[str], q: str, location: str) -> List[Dict[str, Any]]:
    """No API key: direct search pages on the big job sites, one per skill."""
    loc = location or "India"
    items = []
    for s in (skills or [q or "software developer"])[:5]:
        kw = f"{q} {s}".strip() if q and q.lower() != s.lower() else s
        sites = {
            "LinkedIn": f"https://www.linkedin.com/jobs/search/?keywords={quote_plus(kw)}&location={quote_plus(loc)}",
            "Naukri": f"https://www.naukri.com/{_slug(kw)}-jobs-in-{_slug(loc)}",
            "Indeed": f"https://in.indeed.com/jobs?q={quote_plus(kw)}&l={quote_plus(loc)}",
        }
        for site, url in sites.items():
            items.append({
                "id": f"link-{site.lower()}-{_slug(kw)}",
                "title": f"{kw} jobs", "company": f"Search on {site}", "location": loc,
                "url": url, "source": site, "posted": "", "salary_min": None, "salary_max": None,
                "skills_matched": [s] if s in skills else [], "kind": "search",
            })
    return items


@router.get("/jobs")
def jobs(skills: str = Query("", description="comma separated"), q: str = "",
        location: str = "India", page: int = 1):
    sk = [s.strip() for s in skills.split(",") if s.strip()]
    key = f"{sk}|{q}|{location}|{page}"
    hit = _CACHE.get(key)
    if hit and time.time() - hit[0] < CACHE_SECONDS:
        return hit[1]

    note = ""
    if os.getenv("ADZUNA_APP_ID") and os.getenv("ADZUNA_APP_KEY"):
        try:
            data = {"source": "adzuna", "jobs": _adzuna(sk, q, location, page), "note": ""}
            if data["jobs"]:
                _CACHE[key] = (time.time(), data)
                return data
            note = "No live listings matched, showing search links instead."
        except Exception as exc:  # network, bad key, quota ...
            log.error("Adzuna failed: %s", exc)
            note = "Live listings are unavailable right now, showing search links instead."
    else:
        note = "Add ADZUNA keys to .env for live listings. Showing search links for now."
    return {"source": "links", "jobs": _search_links(sk, q, location), "note": note}


class JobRef(BaseModel):
    id: str
    title: str
    company: str = ""
    location: str = ""
    url: str = ""
    source: str = ""


class ApplyRequest(BaseModel):
    user_id: str
    job: JobRef
    skills: List[str] = Field(default_factory=list)


def _summary(items: List[Dict[str, Any]]) -> Dict[str, Any]:
    this_month = datetime.now(timezone.utc).strftime("%Y-%m")
    by_skill, by_month = Counter(), Counter()
    for it in items:
        by_month[it["applied_at"][:7]] += 1
        for s in it.get("skills", []):
            by_skill[s] += 1
    return {"items": items, "total": len(items), "this_month": by_month.get(this_month, 0),
            "by_skill": dict(by_skill), "by_month": dict(by_month)}


@router.post("/applications")
def apply(req: ApplyRequest):
    doc = database.get_doc("applications", req.user_id) or {"items": []}
    items = doc.get("items", [])
    repeatable = req.job.id.startswith("link-")  # a search page can lead to many applications
    if not repeatable and any(i["job"]["id"] == req.job.id for i in items):
        return {**_summary(items), "status": "already_applied"}
    items.append({"job": req.job.model_dump(), "skills": req.skills,
                "applied_at": datetime.now(timezone.utc).isoformat()})
    database.save_doc("applications", req.user_id, {"items": items})
    return {**_summary(items), "status": "saved"}


@router.get("/applications/{user_id}")
def applications(user_id: str):
    doc = database.get_doc("applications", user_id) or {"items": []}
    return _summary(doc.get("items", []))
# ---------- Skill progress (completed skills ticked on the Skill Gap page) ----------
class SkillDone(BaseModel):
    user_id: str
    skill: str
    done: bool = True


def _skill_summary(items: List[Dict[str, Any]]) -> Dict[str, Any]:
    by_month = Counter(i["completed_at"][:7] for i in items)
    return {"items": items, "total": len(items),
            "completed": [i["skill"] for i in items], "by_month": dict(by_month)}


@router.post("/skill-progress")
def set_skill_progress(req: SkillDone):
    doc = database.get_doc("skill_progress", req.user_id) or {"items": []}
    items = doc.get("items", [])
    existing = next((i for i in items if i["skill"].lower() == req.skill.lower()), None)
    if req.done and not existing:
        items.append({"skill": req.skill, "completed_at": datetime.now(timezone.utc).isoformat()})
    elif not req.done and existing:
        items = [i for i in items if i is not existing]
    database.save_doc("skill_progress", req.user_id, {"items": items})
    return _skill_summary(items)


@router.get("/skill-progress/{user_id}")
def get_skill_progress(user_id: str):
    doc = database.get_doc("skill_progress", user_id) or {"items": []}
    return _skill_summary(doc.get("items", []))