from typing import Annotated
from sqlalchemy.orm import Session
from database import SessionLocal
from fastapi import APIRouter, Depends
from src.auth import schema as auth_schema
from src.auth import models as auth_models
from starlette import status
from passlib.context import CryptContext

router = APIRouter()


bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


@router.post("/auth", status_code=status.HTTP_201_CREATED)
async def create_user(
    db: db_dependency, create_user_request: auth_schema.CreateUserRequest
):
    create_user_model = auth_models.User(
        email=create_user_request.email,
        username=create_user_request.username,
        first_name=create_user_request.first_name,
        last_name=create_user_request.last_name,
        role=create_user_request.role,
        hashed_password=bcrypt_context.hash(create_user_request.password),
        is_active=True,
    )

    db.add(create_user_model)
    db.commit()
