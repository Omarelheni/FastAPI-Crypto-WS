from pydantic import BaseModel
class UserLogin(BaseModel):
    email: str
    password: str
    

class UserCreate(BaseModel):
    name : str
    password : str
    email : str
    
    class Config:
        orm_mode = True

class UserUpdate(UserCreate):
    pass

class User(UserCreate):
    id : int


class WatchlistCreate(BaseModel):
    name: str
    symbols: list[str]

    class Config:
        orm_mode = True