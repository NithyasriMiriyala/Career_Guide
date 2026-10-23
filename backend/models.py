"""Data shapes (schemas) for the REST API."""
from typing import Dict, List, Literal, Optional

from pydantic import BaseModel, Field

Level = Literal["Beginner", "Intermediate", "Advanced"]


class Profile(BaseModel):
    user_id: str = Field(..., min_length=1, description="Unique id for this user")
    name: str = ""
    dob: Optional[str] = None                       # "YYYY-MM-DD"
    grad_year: Optional[int] = Field(None, ge=1950, le=2050)
    education: str = ""                              # e.g. "B.Tech, Computer Science"
    interests: List[str] = Field(default_factory=list)
    career_goal: str = ""   
    experience_level: str = ""
    experience: str = ""   
    skills: List[str] = Field(default_factory=list)
    extra_skills: List[str] = Field(default_factory=list)
    levels: Dict[str, Level] = Field(default_factory=dict)    # skill -> current level
    targets: Dict[str, Level] = Field(default_factory=dict)   # skill -> level to reach


class ResumeInput(BaseModel):
    user_id: str = Field(..., min_length=1)
    name: str = ""
    role: str = "AI Engineer"                        # target role
    email: str = ""
    phone: str = ""
    location: str = ""
    linkedin: str = ""
    skills: List[str] = Field(default_factory=list)
    summary: str = ""
    education: str = ""
    experience: str = ""
    projects: str = ""
    certificates: str = ""
    volunteer: str = ""
    hobbies: str = ""


class ProgressUpdate(BaseModel):
    user_id: str = Field(..., min_length=1)
    month: str                                       # e.g. "Oct"
    jobs_applied: int = Field(..., ge=0, le=500)


class ChatRequest(BaseModel):
    user_id: str = Field(..., min_length=1)
    message: str = Field(..., min_length=1, max_length=4000)
    mode: Literal["career", "resume"] = "career"


class ChatResponse(BaseModel):
    reply: str
    sources: List[str] = Field(default_factory=list)
    llm_used: bool = False