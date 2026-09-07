from asgiref import server
from pydantic import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    APP_NAME: str = "point System API"
    DEBUG: bool = False

    DATABASE_URI: str

    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    USER_ROLE: dict = {
        "NORMAL" : "普通用户",
        "COMPANION" : "陪玩",
        "ADMIN" : "管理员",
    }

    class Config:
        env_file = ".env"

settings = Settings()