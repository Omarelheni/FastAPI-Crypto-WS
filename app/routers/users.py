from fastapi import  Depends,APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
import app.service as service
from ..database import get_db,init_db
from ..schemas import UserCreate

router = APIRouter(prefix="/users",tags=["users"]
                   )
@router.get("/")
async def get_users(db : AsyncSession = Depends(get_db)):
    return await service.get_users(db)

@router.post("/")
async def add_user(user : UserCreate,db: AsyncSession = Depends(get_db)):
    user = await service.add_user(db,user)
    return user

