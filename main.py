from fastapi import FastAPI
from enum import IntEnum
from pydantic import BaseModel, Field
from typing import Optional
from fastapi.exceptions import HTTPException
from db_basics import Priority


app = FastAPI()


class TodoCreate(BaseModel):
    task : str = Field(..., min_length=1, max_length=100, description="The task to be done")
    completed: bool = Field(default=False, description="Whether the task is completed or not")
    priority: Priority = Field(default=Priority.MEDIUM, description="Priority of the task")

class Todo(TodoCreate):
    id: int = Field(..., description="Unique identifier for the todo item")

class TodoUpdate(BaseModel):
    task: Optional[str] = Field(None, min_length=1, max_length=100, description="The task to be done")
    completed: Optional[bool] = Field(None, description="Whether the task is completed or not")
    priority: Optional[Priority] = Field(None, description="Priority of the task")


all_todos  =[
    Todo(id=1, task="Buy groceries", completed=False, priority=Priority.MEDIUM),
    Todo(id=2, task="Walk the dog", completed=True, priority=Priority.LOW),
    Todo(id=3, task="Read a book", completed=False, priority=Priority.HIGH),
    Todo(id=4, task="Write code", completed=False, priority=Priority.MEDIUM),
    Todo(id=5, task="Exercise", completed=True, priority=Priority.LOW),
    Todo(id=6, task="Clean the house", completed=False, priority=Priority.HIGH),
]

@app.get("/todos/{todo_id}", response_model=Todo)
def read_root(todo_id: int):
    for todo in all_todos:
        if todo.id == todo_id:
            return todo
    return {"error": "Todo not found"}

@app.get("/todos")
def read_all(first_n: int = None):
    return all_todos[0:first_n] if first_n is not None else all_todos


@app.post("/todos")
def create_todo(todo: TodoCreate):
    new_id = max(todo.id for todo in all_todos) + 1 if all_todos else 1
    todo.id = new_id
    all_todos.append(todo)
    return todo

@app.put("/todos/{todo_id}")
def update_todo(todo_id: int, updated_todo: TodoUpdate):
    for todo in all_todos:
        if todo.id == todo_id:
            for key, value in updated_todo.model_dump(exclude_unset=True).items():
                setattr(todo, key, value)
            return todo
    raise HTTPException(status_code=404, detail="Todo not found")

@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):
    if not any(todo.id == todo_id for todo in all_todos):
        raise HTTPException(status_code=404, detail="Todo not found")
    global all_todos
    all_todos = [todo for todo in all_todos if todo.id != todo_id]
    return {"message": "Todo deleted successfully"}
    