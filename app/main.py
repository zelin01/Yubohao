from fastapi import FastAPI
from app.database import engine, Base
from app.routers import auth, users, wallet

app = FastAPI(title="点单系统后端")

@app.on_event("startup")
async def init():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(wallet.router)