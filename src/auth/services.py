import os
import uuid
import jwt
from datetime import datetime, timedelta, timezone
from typing import Any, Literal
from dotenv import load_dotenv
from passlib.context import CryptContext
from src.account.models import User
from src.account.repositories import UserRepository
from src.account.schemas import UserResponseSchema
from src.core.db import DbSession
from src.core.exceptions import InternalInvariantError

load_dotenv()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY: str = os.getenv("SECRET_KEY", default="")
ALGORITHM: str = os.getenv("ALGORITHM", default="")

if not SECRET_KEY or not ALGORITHM:
    raise InternalInvariantError(
        "Missing SECRET_KEY or ALGORITHM in .env file."
    )


class AuthService:
    @staticmethod
    def verify_password(plain_password, hashed_password) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    # @staticmethod
    # def get_user_by_email(db: DbSession, email: str) -> User | None:
    #     user: User | None = db.scalar(
    #         select(User).where(
    #             User.email == email
    #         )
    #     )

    #     return user

    @staticmethod
    def authenticate_user(
        db: DbSession, email: str, password: str
    ) -> UserResponseSchema | Literal[False]:
        user: User | None = UserRepository.get_user_by_email(db, email)
        if not user or not AuthService.verify_password(
            password,
            user.password
        ):
            return False
        return UserResponseSchema.model_validate(user)

    @staticmethod
    def create_access_token(
        user_id: uuid.UUID, expires_delta: timedelta | None = None
    ) -> str:
        if expires_delta:
            expire: datetime = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=15)

        to_encode: dict[str, Any] = {
            "user_id": str(user_id),
            "exp": expire,
        }

        encoded_jwt: str = jwt.encode(
            to_encode,
            SECRET_KEY, algorithm=ALGORITHM
        )

        return encoded_jwt
