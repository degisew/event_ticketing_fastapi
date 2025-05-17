import uuid
from typing import Annotated, List
from fastapi import APIRouter, Depends, Request, status
from fastapi.security import OAuth2PasswordBearer

from src.account.schemas import (
    BaseUserSchema,
    UserSchema,
    UserResponseSchema,
)

from src.account.services import UserService
from src.core.db import DbSession

router = APIRouter(prefix="/users", tags=["Account"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")

oauth_token_bearer = Annotated[str, Depends(oauth2_scheme)]


@router.post(
    "/",
    response_model=UserResponseSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_user(db: DbSession, user: UserSchema) -> UserResponseSchema:
    """
    Create a new user.
    """
    return UserService.create_user(db, user)


@router.get("/")
async def get_users(db: DbSession) -> List[UserResponseSchema]:
    """
    Get all users.
    """
    return UserService.get_users(db)


@router.get("/profile")
async def get_current_user_profile(
    db: DbSession, token: oauth_token_bearer
) -> UserResponseSchema:
    return UserService.get_current_user(db, token)


@router.get("/{user_id}", response_model=UserResponseSchema)
async def get_user(db: DbSession, user_id: uuid.UUID) -> UserResponseSchema:
    """
    Get user by ID.
    """
    return UserService.get_user(db, user_id)


@router.patch("/{user_id}", response_model=UserResponseSchema)
async def update_user(db: DbSession, user_id: uuid.UUID, user: BaseUserSchema):
    """
    Update an existing user.
    """
    return UserService.update_user(db, user_id, user)
