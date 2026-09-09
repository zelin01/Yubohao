from asyncio import set_event_loop

from fastapi import APIRouter, Depends, HTTPException, status
from six import assertNotRegex
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.models import User, UserRole
from app.schemas import RegisterIn, LoginIn, TokenOut
from app.security import hash_password, verify_password, create_token

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", status_code = status.HTTP_201_CREATED)
async def register(data: RegisterIn, db: AsyncSession = Depends(get_db)):
    if data.role == UserRole.ADMIN:
        raise HTTPException(403, "Admin privilege")
    exists = (await db.execute(
        select(User.id).where(User.username == data.username)
    )).scalar_one_or_none()
    if exists:
        raise HTTPException(409, "User already exists")
    user = User(
        username=data.username,
        password_hash=hash_password(data.password),
        nickname=data.nickname,
        role=data.role,
    )
    db.add(user)
    await db.commit()
    return {"id": user.id, "username": user.username}

@router.post("/login", response_model=TokenOut)
async def login(data: LoginIn, db: AsyncSession = Depends(get_db)):
    user = (await db.execute(
        select(User).where(User.username == data.username)
    )).scalar_one_or_none()
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Incorrect password")
    return TokenOut(access_token=create_token(user.id))