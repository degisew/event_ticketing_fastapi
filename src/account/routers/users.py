import uuid
from typing import List
from fastapi import APIRouter, status

from src.account.schemas.users import (
    BaseUserSchema,
    UserSchema,
    UserResponseschema
)


router = APIRouter(prefix="/users", tags=["account"])


@router.get("/")
async def get_users() -> List[UserResponseschema]:
    """
    Get all users.
    """
    return []


@router.get(
    "/{user_id}",
    response_model=UserResponseschema
)
async def get_user(user_id: uuid.UUID) -> dict[str, str]:
    """
    Get user by ID.
    """
    return {"user": "user {user_id}"}


@router.post(
    "/",
    response_model=UserResponseschema,
    status_code=status.HTTP_201_CREATED,
)
async def create_user(user: UserSchema) -> UserSchema:
    """
    Create a new user.
    """
    return user


@router.patch("/{user_id}", response_model=UserResponseschema)
async def update_user(user_id: uuid.UUID, user: BaseUserSchema):
    """
    Update an existing user.
    """
    return user
