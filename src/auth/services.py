import os
import uuid
import jwt
from datetime import datetime, timedelta, timezone
from typing import Annotated, Any, Literal
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from dotenv import load_dotenv
from passlib.context import CryptContext
from sqlalchemy import select
from src.account.models import User
from src.account.schemas import UserInDBSchema
from src.account.services import UserService
from src.auth.schemas import TokenData
from src.core.db import DbSession
from src.core.exceptions import (
    AuthenticationErrorException,
    InternalInvariantError,
    NotFoundException,
)

load_dotenv()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

# oauth_token_scheme = Annotated[str, Depends(oauth2_scheme)]

SECRET_KEY: str = os.getenv("SECRET_KEY", default="")
ALGORITHM: str = os.getenv("ALGORITHM", default="")

if not SECRET_KEY or not ALGORITHM:
    raise InternalInvariantError("Missing SECRET_KEY or ALGORITHM in .env file.")


class AuthService:
    @staticmethod
    def verify_password(plain_password, hashed_password) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def authenticate_user(
        db: DbSession, email: str, password: str
    ) -> UserInDBSchema | Literal[False]:
        user: UserInDBSchema | None = UserService.get_user_by_email(db, email)
        if not user or not AuthService.verify_password(
            password,
            user.password
        ):
            return False
        return user

    @staticmethod
    def create_access_token(
        email: str, user_id: uuid.UUID, expires_delta: timedelta | None = None
    ) -> str:
        if expires_delta:
            expire: datetime = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=15)

        to_encode: dict[str, Any] = {
            "sub": email,
            "id": str(user_id),
            "exp": expire,
        }

        encoded_jwt: str = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

        return encoded_jwt

    # @staticmethod
    # async def get_current_user(db: DbSession, token: oauth_token_scheme):
    #     try:
    #         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    #         email = payload.get("sub")
    #         if not email:
    #             raise AuthenticationErrorException()
    #         token_data = TokenData(email=email)
    #     except jwt.InvalidTokenError:
    #         raise AuthenticationErrorException()
    #     user: UserInDBSchema = AuthService.get_user(db=db, email=token_data.email)
    #     if not user:
    #         raise AuthenticationErrorException()
    #     return user

    # current_user = Annotated[TokenData, Depends(get_current_user)]
