from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from .models import User

from .schemas import UserCreate, WatchlistCreate

async def get_users(db: AsyncSession):
    result = await db.execute(select(User))
    return result.scalars().all()

async def add_user(db: AsyncSession,user: UserCreate):
    db_user = User(name=user.name, email=user.email, password="")
    db_user.set_password(user.password)  # Hash le mot de passe avant de le stocker
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

async def get_watchlists_symbols_by_user_id(db: AsyncSession, user_id: int):
    result = await db.execute(select(User.prefered_symbols).where(User.id == user_id))
    prefered_symbols = result.scalar_one_or_none()
    return prefered_symbols

async def get_user_by_email(db: AsyncSession, email: str):
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()
    return user

async def add_watchlist(db: AsyncSession, watchlist: WatchlistCreate, user_id:int):
    db_watchlist = Watchlist(
        name=watchlist.name,
        symbols=watchlist.symbols,
        user_id=user_id
    )

    db.add(db_watchlist)

    await db.commit()
    await db.refresh(db_watchlist)

    return db_watchlist