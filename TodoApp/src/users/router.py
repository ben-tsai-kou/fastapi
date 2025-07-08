from typing import Annotated
from sqlalchemy.orm import Session
from database import SessionLocal
from fastapi import APIRouter, Depends
from starlette import status
from fastapi import HTTPException
from src.auth import router as auth_router
from passlib.context import CryptContext
from src.auth import models as auth_models
from src.users import schema as users_schema

router = APIRouter(prefix="/user", tags=["user"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(auth_router.get_current_user)]
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.get("/", status_code=status.HTTP_200_OK)
async def get_user(user: user_dependency, db: db_dependency):
    return (
        db.query(auth_models.Users)
        .filter(auth_models.Users.id == user.get("id"))
        .first()
    )


@router.put("/password", status_code=status.HTTP_204_NO_CONTENT)
async def change_password(
    user: user_dependency,
    db: db_dependency,
    user_verification: users_schema.UserVerification,
):
    user_model = (
        db.query(auth_models.Users)
        .filter(auth_models.Users.id == user.get("id"))
        .first()
    )

    if not bcrypt_context.verify(
        user_verification.password, user_model.hashed_password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Error on password change"
        )
    user_model.hashed_password = bcrypt_context.hash(user_verification.new_password)
    db.commit()
