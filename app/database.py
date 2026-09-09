# 异步数据库连接
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from app.config import settings

# 创建异步引擎
engine = create_async_engine(settings.DATABASE_URI, echo = False)

# 创建Session工厂
SessionLocal = async_sessionmaker(engine, expire_on_commit = False)

# 声明 ORM 模型基类
class Base(DeclarativeBase):
    pass

# 依赖注入生成器
async def get_db():
    async with SessionLocal() as session:
        yield session