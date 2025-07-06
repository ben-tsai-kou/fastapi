from fastapi import APIRouter
from src.auth import schema as auth_schema
from src.auth import models as auth_models

router = APIRouter()


@router.post("/auth")
async def create_user(create_user_request: auth_schema.CreateUserRequest):
    create_user_model = auth_models.User(
        email=create_user_request.email,
        username=create_user_request.username,
        first_name=create_user_request.first_name,
        last_name=create_user_request.last_name,
        role=create_user_request.role,
        hashed_password=create_user_request.password,
        is_active=True,
    )
    return create_user_model
