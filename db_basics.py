from sqlalchemy import create_engine, MetaData, Column, Integer, String, Table, ForeignKey,Enum
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from enum import IntEnum

engine = create_engine("sqlite:///./todos.db",echo=True)

Base = declarative_base()

meta = MetaData()


class Priority(IntEnum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3


class Person(Base):
    __tablename__ = 'people'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    age = Column(Integer)

    todos = relationship("Todo", back_populates="person")


class Todo(Base):
    __tablename__ = 'todos'
    id = Column(Integer, primary_key=True, index=True)
    task = Column(String, index=True)
    completed = Column(Integer)
    priority = Column(Enum(Priority), default=Priority.MEDIUM)
    person_id = Column(Integer,ForeignKey("people.id"))

    person = relationship("Person", back_populates="todos")

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


result = session.query(Person.age,Todo.task).join(Todo).all()

print(result)
 