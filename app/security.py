from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext
from app.config import settings

pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 生成密码哈希
def hash_password(pwd: str) -> str:
    return pwd_ctx.hash(pwd)

# 登录校验
def verify_password(pwd: str, hashed: str) -> bool:
    return pwd_ctx.verify(pwd, hashed)

# 生成访问令牌
def create_token(user_id: int) -> str:
    payload = {
        "sub": str(user_id), # 令牌归属者
        "exp": datetime.now() + timedelta(minutes=settings.JWT_EXPIRATION_MINUTES), # 过期时间
    }
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)

def decode_token(token: str) -> str:
    payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
    return payload["sub"]