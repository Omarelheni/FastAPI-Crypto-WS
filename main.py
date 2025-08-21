from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.database import get_db,init_db
from app.routers import users,coins
from app.tasks import broadcast_task
import asyncio

@asynccontextmanager
async def lifespan(app:FastAPI):
    await init_db()
    asyncio.create_task(broadcast_task())
    
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(coins.router)  # on inclut le router
app.include_router(users.router)