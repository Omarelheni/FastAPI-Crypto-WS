from pydantic import BaseModel

class UserCreate(BaseModel):
    name : str

class UserUpdate(UserCreate):
    pass

class User(UserCreate):
    id : int