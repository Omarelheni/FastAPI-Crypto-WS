from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.database import get_db
from app.routers import users,coins
from app.tasks import broadcast_task
import asyncio
from app.subscriber import redis_subscriber

@asynccontextmanager
async def lifespan(app:FastAPI):
    asyncio.create_task(broadcast_task())
    asyncio.create_task(redis_subscriber())
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(coins.router)  # on inclut le router
app.include_router(users.router)