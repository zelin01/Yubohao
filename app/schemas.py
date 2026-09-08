from datetime import datetime
from pydantic import BaseModel, Field, field_validator
from app.models import UserRole, TxnType

class RegisterIn(BaseModel):
    username: str = Field(min_length=1, max_length=32, pattern=r'^[a-zA-Z0-9_-]+$') # 用户名只允许字母、数字、下划线、连字符
    password: str = Field(min_length=1, max_length=64)
    nickname: str = Field(min_length=1, max_length=32)
    role: UserRole = UserRole.USER

class LoginIn(BaseModel):
    username: str
    password: str

class TokenOut(BaseModel):
    access_token: str
    token_type: str = 'bearer'

class UserOut(BaseModel):
    id: int
    username: str
    nickname: str
    role: UserRole
    avatar_url: str
    balance: float
    created_at: datetime

    model_config = {"from_attributes": True}

class UserUpdateIn(BaseModel):
    nickname: str | None = Field(default=None, min_length=1, max_length=32)
    avatar: str | None = Field(default=None, max_length=255)

# 用户充值请求
class RechargeIn(BaseModel):
    amount: float = Field(gt=0, le=100) # 充值金额限制

    @field_validator("amount")
    @classmethod
    def two_decimals(cls, v: float) -> float:
        if round(v, 2) != v:
            raise ValueError("金额最多两位小数")
        return v

class TxnOut(BaseModel):
    id: int
    amount: float
    type: TxnType
    balance_after: float
    remark: str | None
    created_at: datetime

    model_config = {"from_attributes": True}