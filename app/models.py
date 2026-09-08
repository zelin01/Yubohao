import enum
from datetime import datetime
from sqlalchemy import String, Integer, Numeric, DateTime, ForeignKey, Enum, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

class UserRole(str, enum.Enum):
    USER = "user"          # 普通用户
    COMPANION = "companion"  # 陪玩师
    ADMIN = "admin"

class TxnType(str, enum.Enum):
    RECHARGE = "recharge"  # 充值
    CONSUME = "consume"    # 消费
    INCOME = "income"      # 陪玩师收入
    REFUND = "refund"

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(32), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(128))
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), default=UserRole.USER)
    nickname: Mapped[str] = mapped_column(String(32))
    avatar: Mapped[str | None] = mapped_column(String(255), nullable=True)
    balance: Mapped[float] = mapped_column(Numeric(10, 2), default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

class Transaction(Base):
    __tablename__ = "transactions"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    amount: Mapped[float] = mapped_column(Numeric(10, 2))   # 正=入账 负=出账
    type: Mapped[TxnType] = mapped_column(Enum(TxnType))
    balance_after: Mapped[float] = mapped_column(Numeric(10, 2))
    remark: Mapped[str | None] = mapped_column(String(128), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())