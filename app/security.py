from datetime import datetime, timedelta
import jwt
import bcrypt
from app.config import settings


# 生成密码哈希
def hash_password(pwd: str) -> str:
    return bcrypt.hashpw(pwd.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

# 登录校验
def verify_password(pwd: str, hashed: str) -> bool:
    return bcrypt.checkpw(pwd.encode("utf-8"), hashed.encode("utf-8"))

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