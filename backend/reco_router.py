from typing import List

from fastapi import APIRouter
from pydantic import BaseModel

from .recommender import recommend

router = APIRouter()


class RecoRequest(BaseModel):
    skills: List[str] = []
    career_goal: str = ""
    interests: List[str] = []


@router.post("/recommend")
def recommend_roles(req: RecoRequest):
    return {"engine": "scikit-learn", "roles": recommend(req.skills, req.career_goal, req.interests)}