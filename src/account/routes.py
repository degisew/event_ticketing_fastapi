import uuid
from typing import Any
from fastapi import APIRouter, status

from src.account.schemas import UserSchema, UserResponseschema


router = APIRouter()


@router.get("/users", tags=["account"], response_model=UserResponseschema)
async def get_users() -> dict[str, Any]:
    """
    Get all users.
    """
    return {}


@router.get("users/{user_id}", tags=["account"],)
async def get_user(user_id: uuid.UUID) -> dict[str, str]:
    """
    Get user by ID.
    """
    return {"user": "user {user_id}"}


@router.post(
    "/users",
    tags=["account"],
    response_model=UserResponseschema,
    status_code=status.HTTP_201_CREATED
)
async def create_user(user: UserSchema) -> dict[str, str]:
    """
    Create a new user.
    """
    return {"user": "created user"}


@router.patch("/users/{user_id}", tags=["account"],)
async def update_user(user_id: uuid.UUID):
    """
    Update an existing user.
    """
    return {user_id: "updated user"}
