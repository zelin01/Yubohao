from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.deps import get_current_user
from app.models import User, Transaction, TxnType
from app.schemas import RechargeIn, TxnOut

router = APIRouter(prefix="/wallet", tags=["钱包"])

@router.post("/recharge")
async def recharge(
    data: RechargeIn,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    async with db.begin():  # 事务：锁行 → 加钱 → 记流水
        fresh = (await db.execute(
            select(User).where(User.id == user.id).with_for_update()
        )).scalar_one()
        fresh.balance = float(fresh.balance) + data.amount
        txn = Transaction(
            user_id=fresh.id,
            amount=data.amount,
            type=TxnType.RECHARGE,
            balance_after=fresh.balance,
            remark="充值",
        )
        db.add(txn)
    return {"balance": fresh.balance}

@router.get("/transactions", response_model=list[TxnOut])
async def list_transactions(
    page: int = 1,
    size: int = 20,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    page, size = max(page, 1), min(max(size, 1), 100)
    result = await db.execute(
        select(Transaction)
        .where(Transaction.user_id == user.id)
        .order_by(Transaction.id.desc())
        .offset((page - 1) * size)
        .limit(size)
    )
    return result.scalars().all()