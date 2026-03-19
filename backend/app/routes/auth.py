from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.supabase_client import get_supabase

router = APIRouter(prefix="/api/auth", tags=["auth"])


class AuthRequest(BaseModel):
    email: str
    password: str


class AuthResponse(BaseModel):
    access_token: str
    user_id: str


@router.post("/signup")
async def signup(req: AuthRequest) -> AuthResponse:
    try:
        db = get_supabase()
        result = db.auth.sign_up({"email": req.email, "password": req.password})
        return AuthResponse(access_token=result.session.access_token, user_id=result.user.id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login")
async def login(req: AuthRequest) -> AuthResponse:
    try:
        db = get_supabase()
        result = db.auth.sign_in_with_password({"email": req.email, "password": req.password})
        return AuthResponse(access_token=result.session.access_token, user_id=result.user.id)
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))
