from fastapi import APIRouter, Depends, HTTPException, Path
from src.todo import models as todo_models
from src.todo import schema as todo_schema
from database import SessionLocal
from sqlalchemy.orm import Session
from typing import Annotated
from starlette import status
from src.auth import router as auth_router

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(auth_router.get_current_user)]


@router.get("/", status_code=status.HTTP_200_OK)
async def read_all(user: user_dependency, db: db_dependency):
    return (
        db.query(todo_models.Todos)
        .filter(todo_models.Todos.owner_id == user.get("id"))
        .all()
    )


@router.get("/todo/{todo_id}", status_code=status.HTTP_200_OK)
async def read_todo(
    user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)
):
    todo_model = (
        db.query(todo_models.Todos)
        .filter(todo_models.Todos.id == todo_id)
        .filter(todo_models.Todos.owner_id == user.get("id"))
        .first()
    )
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")


@router.post("/todo", status_code=status.HTTP_201_CREATED)
async def create_todo(
    user: user_dependency, db: db_dependency, todo_request: todo_schema.TodoRequest
):
    todo_model = todo_models.Todos(**todo_request.model_dump(), owner_id=user.get("id"))
    db.add(todo_model)
    db.commit()


@router.put("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(
    user: user_dependency,
    db: db_dependency,
    todo_request: todo_schema.TodoRequest,
    todo_id: int = Path(gt=0),
):
    todo_model = (
        db.query(todo_models.Todos)
        .filter(todo_models.Todos.id == todo_id)
        .filter(todo_models.Todos.owner_id == user.get("id"))
        .first()
    )
    if todo_model is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="todo not found."
        )

    for key, value in todo_request.model_dump(exclude={"id"}).items():
        setattr(todo_model, key, value)

    db.commit()


@router.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(
    user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)
):
    todo_model = (
        db.query(todo_models.Todos)
        .filter(todo_models.Todos.id == todo_id)
        .filter(todo_models.Todos.owner_id == user.get("id"))
        .first()
    )
    if todo_model is None:
        raise HTTPException(status_code=404, detail="todo not found")

    db.delete(todo_model)
    db.commit()
