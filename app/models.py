from sqlalchemy import create_engine, MetaData, Column, Integer, String, Table, ForeignKey, Enum
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from enum import IntEnum
from passlib.context import CryptContext

Base = declarative_base()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    password = Column(String)
    email = Column(String, unique=True, index=True)

    def set_password(self, plain_password: str):
        """Hash le mot de passe et le stocke dans l'objet."""
        self.password = pwd_context.hash(plain_password)

    def verify_password(self, plain_password: str) -> bool:
        """Vérifie que le mot de passe correspond au hash."""
        return pwd_context.verify(plain_password, self.password)
