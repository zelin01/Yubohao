import enum
from datetime import datetime
from sqlalchemy import String, Numeric, DateTime, ForeignKey, Enum, func
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base

# 定义用户模型
class UserRole(str, enum.Enum):
    USER = "user"          # 普通用户
    COMPANION = "companion"  # 陪玩师
    ADMIN = "admin"

# 定义资金模型
class TxnType(str, enum.Enum):
    RECHARGE = "recharge"  # 充值
    CONSUME = "consume"    # 消费
    INCOME = "income"      # 陪玩师收入
    REFUND = "refund"

# 创建用户表
class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(32), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(128))
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), default=UserRole.USER) # 用户类型
    nickname: Mapped[str] = mapped_column(String(32)) # 用户昵称
    avatar: Mapped[str | None] = mapped_column(String(255), nullable=True) # 头像
    balance: Mapped[float] = mapped_column(Numeric(10, 2), default=0) # 余额
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

# 创建资金流水表
class Transaction(Base):
    __tablename__ = "transactions"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True) # 外键指向Users表id行
    amount: Mapped[float] = mapped_column(Numeric(10, 2))   # 正=入账 负=出账
    type: Mapped[TxnType] = mapped_column(Enum(TxnType))
    balance_after: Mapped[float] = mapped_column(Numeric(10, 2))
    remark: Mapped[str | None] = mapped_column(String(128), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())