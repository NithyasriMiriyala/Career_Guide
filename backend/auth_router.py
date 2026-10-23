from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from . import auth

router = APIRouter()


class Credentials(BaseModel):
    email: str
    password: str


@router.post("/auth/register")
def register(c: Credentials):
    try:
        return {"uid": auth.register(c.email, c.password)}
    except auth.AuthError as e:
        raise HTTPException(status_code=e.status, detail=e.message)


@router.post("/auth/login")
def login(c: Credentials):
    try:
        return {"uid": auth.login(c.email, c.password)}
    except auth.AuthError as e:
        raise HTTPException(status_code=e.status, detail=e.message)