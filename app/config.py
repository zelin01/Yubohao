from pydantic import BaseSettings, SettingsConfigDIct

class Settings(BaseSettings):
    DATABASE_URL: str
    JWT_SECRET: str
    JWT_EXPIRE_MINUTES: int
    ALGORITHMS: str = 'HS256'

    model_config = SettingsConfigDIct(env_file = ".env")

settings = Settings()