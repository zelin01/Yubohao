
from sqlalchemy import Column, Integer, String, Float, DateTime, Enum, Boolean, Table, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from Order_meal.app.core.database import Base
import enum

class UserRole(str, enum.Enum):
    NORMAL = "normal"
    COMPANION = "companion"
    ADMIN = "admin"

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index = True)
    username = Column(String(50), unique=True, index = True, nullable = False)
    telephone = Column(String(11), unique=True,nullable = False)
    password_hash = Column(String(255), nullable = False)
    full_name = Column(String(20), nullable = False)

    role = Column(Enum(UserRole), default=UserRole.NORMAL, nullable = False)
    is_active = Column(Boolean, default = True, nullable = False)
    is_verified = Column(Boolean, default = False, nullable = False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_login_at = Column(DateTime(timezone=True), nullable = True)

    transactions = relationship("Transaction", back_populates="user")

    def __repr__(self):
        return f"<User {self.username}>"
