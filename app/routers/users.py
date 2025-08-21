from fastapi import  Depends,APIRouter, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
import app.service as service
from ..database import get_db
from ..schemas import UserCreate, UserLogin
from app.auth import create_access_token
import websockets

router = APIRouter(prefix="/users",tags=["users"])


@router.get("/")
async def get_users(db : AsyncSession = Depends(get_db)):
    return await service.get_users(db)

@router.post("/")
async def add_user(user : UserCreate,db: AsyncSession = Depends(get_db)):
    user = await service.add_user(db,user)
    return user


@router.post("/login")
async def login(user: UserLogin, db: AsyncSession = Depends(get_db)):
    user_db = await service.get_user_by_email(db, user.email)
    if not user_db:
        raise HTTPException(status_code=404, detail="User not found")
    if not user_db.verify_password(user.password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    token = create_access_token({"id": user_db.id, "email": user_db.email, "name": user_db.name})
    return {"access_token": token}