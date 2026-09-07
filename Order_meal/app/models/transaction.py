from sqlalchemy import Column, Integer, String, Float, DateTime, Enum, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from Order_meal.app.core.database import Base
import enum

class TransactionType(str, enum.Enum):
    RECHARGE = "recharge"
    CONSUME = "consume"

class TransactionStatus(str, enum.Enum):
    PENDING = "pending"
    SUCCESS = "success"
    FAILED = "failed"
    CANCELED = "canceled"

class Transaction(Base):
    __tablename__ = "transaction"

    id = Column(Integer, primary_key=True, index=True)
    transaction_on = Column(String(50), unique=True, index=True, nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)

    payment_method = Column(String(50), nullable=False)
    third_party_transaction = Column(String(50), nullable=False)

    description = Column(String(50), nullable=False)
    remark = Column(Text, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)

    user = relationship("User", back_populates="transactions")