import uuid
from typing import List
from fastapi import APIRouter, status
from src.account.dependencies import CurrentUser

from src.account.schemas import (
    UpdateUserSchema,
    UserSchema,
    UserResponseSchema,
)

from src.account.services import UserService
from src.core.db import DbSession
from src.event.schemas.reservation import ReservationResponseSchema
from src.event.services.reservation import ReservationService

router = APIRouter(prefix="/users", tags=["Account"])


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
    db: DbSession, current_user: CurrentUser
) -> UserResponseSchema:
    return current_user


@router.patch("/profile/edit", response_model=UserResponseSchema)
async def update_user(db: DbSession, current_user: CurrentUser, user: UpdateUserSchema):
    """
    Update user profile.
    """
    return UserService.update_user(db, current_user.id, user)


@router.get("/{user_id}", response_model=UserResponseSchema)
async def get_user(db: DbSession, user_id: uuid.UUID) -> UserResponseSchema:
    """
    Get user by ID.
    """
    return UserService.get_user(db, user_id)
