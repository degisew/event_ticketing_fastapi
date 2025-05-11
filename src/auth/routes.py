import os
from datetime import timedelta
from dotenv import load_dotenv
from typing import Annotated
from fastapi import Depends
from fastapi.routing import APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from src.auth.schemas import TokenSchema
from src.auth.services import AuthService
from src.core.db import DbSession
from src.core.exceptions import AuthenticationErrorException


router = APIRouter(prefix="/auth")

load_dotenv()

ACCESS_TOKEN_EXPIRE_MINUTES: int = int(
    os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 0))


@router.post("/token")
async def login_for_access_token(
    db: DbSession,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> TokenSchema:
    user = AuthService.authenticate_user(
        db, form_data.username, form_data.password)

    if not user:
        raise AuthenticationErrorException()
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token: str = AuthService.create_access_token(
        user_id=user.id, expires_delta=access_token_expires
    )

    obj: dict[str, str] = {
        "access_token": access_token,
        "token_type": "bearer"
    }

    return TokenSchema.model_validate(obj)
