from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from .models import User
from .schemas import UserCreate

async def get_users(db: AsyncSession):
    result = await db.execute(select(User))
    return result.scalars().all()

async def add_user(db: AsyncSession,user: UserCreate):
    db_user = User(name=user.name)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user
