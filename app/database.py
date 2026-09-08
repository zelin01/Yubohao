from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeMeta
from app.config import settings

engine = create_async_engine(settings.DATABASE_URI, echo = False)
SessionLocal = async_sessionmaker(engine, expire_on_commit = False)

class Base(DeclarativeMeta):
    pass

async def get_db():
    async with engine.begin() as session:
        yield session