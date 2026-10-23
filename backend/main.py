"""Run:  python -m uvicorn backend.main:app --reload --port 8000"""
from .jobs_router import router as jobs_router
from .auth_router import router as auth_router
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from utils.ats import build_resume_text, score_resume
from utils.local_matcher import ROLES, match_roles
from utils.roadmap import topics_for

from . import config, database, rag
from .models import ChatRequest, ChatResponse, Profile, ProgressUpdate, ResumeInput
from .reco_router import router as reco_router
from .assistant import quick_answer

logging.basicConfig(level=logging.INFO)
LEVELS = ["Beginner", "Intermediate", "Advanced"]


@asynccontextmanager
async def lifespan(app: FastAPI):
    database.init_db()  # connect once when the server starts
    yield


app = FastAPI(title="CareerGuide AI", version="1.0.0", lifespan=lifespan)
app.include_router(auth_router)
app.include_router(reco_router)
app.include_router(jobs_router)

# CORS: allowed origins come from CORS_ORIGINS in .env (local + live URLs)
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def _profile_or_404(user_id: str) -> dict:
    p = database.get_doc("profiles", user_id)
    if not p:
        raise HTTPException(404, "Profile not found. Save a profile first.")
    return p


def _all_skills(p: dict) -> list:
    return p.get("skills", []) + p.get("extra_skills", [])


# ---------------- Basics ----------------
@app.api_route("/health", methods=["GET", "HEAD"])
def health():
    return {"status": "ok", "database": database.backend_name(),
            "llm_enabled": bool(config.ANTHROPIC_API_KEY)}


@app.get("/roles")
def roles():
    return sorted(ROLES.keys())


# ---------------- Profile ----------------
@app.put("/profiles")
def save_profile(profile: Profile):
    return database.save_doc("profiles", profile.user_id, profile.model_dump())


@app.get("/profiles/{user_id}")
def get_profile(user_id: str):
    return _profile_or_404(user_id)


# ---------------- Recommendations ----------------
@app.get("/recommendations/{user_id}")
def recommendations(user_id: str, top_n: int = 6):
    p = _profile_or_404(user_id)
    return match_roles(_all_skills(p))[:top_n]


# ---------------- Skill gap ----------------
@app.get("/skill-gap/{user_id}")
def skill_gap(user_id: str):
    p = _profile_or_404(user_id)
    items = []
    for s in _all_skills(p):
        cur = p.get("levels", {}).get(s, "Beginner")
        tgt = p.get("targets", {}).get(s, "Advanced")
        items.append({"skill": s, "current": cur, "target": tgt,
                    "levels_to_go": max(0, LEVELS.index(tgt) - LEVELS.index(cur))})
    to_improve = sum(1 for i in items if i["levels_to_go"] > 0)
    return {"known": len(items), "to_improve": to_improve,
            "reached": len(items) - to_improve, "skills": items}


# ---------------- Learning roadmap (topics only) ----------------
@app.get("/roadmap/{user_id}")
def roadmap(user_id: str):
    p = _profile_or_404(user_id)
    plan = []
    for s in _all_skills(p):
        cur = p.get("levels", {}).get(s, "Beginner")
        tgt = p.get("targets", {}).get(s, "Advanced")
        ci, ti = LEVELS.index(cur), LEVELS.index(tgt)
        if ti <= ci:
            continue
        stages = [{"from": LEVELS[LEVELS.index(lv) - 1], "to": lv, "topics": topics_for(s, lv)}
                for lv in LEVELS[ci + 1: ti + 1]]
        plan.append({"skill": s, "current": cur, "target": tgt, "stages": stages})
    return {"skills_to_improve": len(plan), "plan": plan}


# ---------------- Resume builder + ATS score ----------------
@app.post("/resume")
def make_resume(data: ResumeInput):
    if data.role not in ROLES:
        raise HTTPException(422, f"Unknown role '{data.role}'. Use GET /roles for valid roles.")
    d = data.model_dump()
    result = score_resume(d, data.role)
    text = build_resume_text(d, data.role)
    database.save_doc("resumes", data.user_id, d)
    return {"ats_score": result["total"], "breakdown": result["parts"],
            "resume_text": text, "jobs": match_roles(data.skills)[:3]}


@app.get("/resume/{user_id}")
def get_resume(user_id: str):
    d = database.get_doc("resumes", user_id)
    if not d:
        raise HTTPException(404, "No resume saved yet.")
    return d


# ---------------- Progress chart data ----------------
@app.put("/progress")
def update_progress(update: ProgressUpdate):
    doc = database.get_doc("progress", update.user_id) or {"data": []}
    rows = [r for r in doc["data"] if r["month"] != update.month]
    rows.append({"month": update.month, "jobs_applied": update.jobs_applied})
    database.save_doc("progress", update.user_id, {"data": rows})
    return rows


@app.get("/progress/{user_id}")
def get_progress(user_id: str):
    return (database.get_doc("progress", user_id) or {"data": []})["data"]


# ---------------- Chat (placeholder until the RAG step) ----------------
# ---------------- Chat (RAG) ----------------
@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    profile = database.get_doc("profiles", req.user_id) or {}  # optional context
    history = database.get_chat(req.user_id)

    quick = quick_answer(req.message, profile)
    if quick:
        reply, sources, used = quick, ["CareerGuide assistant"], False
    else:
        reply, sources, used = rag.answer(req.message, profile, history, req.mode)

    database.append_chat(req.user_id, "user", req.message)
    database.append_chat(req.user_id, "assistant", reply)
    return ChatResponse(reply=reply, sources=sources, llm_used=used)


@app.get("/chat/{user_id}")
def chat_history(user_id: str):
    return database.get_chat(user_id, limit=50)