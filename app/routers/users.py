from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.deps import get_current_user
from app.models import User
from app.schemas import UserOut, UserUpdateIn
from starlette import status

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/me", response_model=UserOut)
async def get_me(user: User = Depends(get_current_user)):
    return user

@router.patch("/me", response_model=UserOut)
async def update_me(
        data: UserUpdateIn,
        user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db),
):
    if data.nickname is not None:
        user.nickname = data.nickname
    if data.avatar is not None:
        user.avatar = data.avatar
    await db.commit()
    await db.refresh(user)
    return user

