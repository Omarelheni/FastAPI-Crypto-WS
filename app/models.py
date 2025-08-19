from sqlalchemy import create_engine, MetaData, Column, Integer, String, Table, ForeignKey,Enum
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from enum import IntEnum

Base = declarative_base()

class Priority(IntEnum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True,index=True)
    name = Column(String , index=True)

 