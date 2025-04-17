import os
from datetime import datetime, timedelta, timezone
from typing import Annotated, Any
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from dotenv import load_dotenv
from sqlalchemy import select
from src.account.models import User
from src.account.schemas import UserInDBSchema
from src.auth.schemas import SignInSchema, TokenData
from src.core.db import DbSession
from src.core.exceptions import NotFoundException
from passlib.context import CryptContext

load_dotenv()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

oauth_token_scheme = Annotated[str, Depends(oauth2_scheme)]

SECRET_KEY: str = os.getenv("SECRET_KEY", default="")
ALGORITHM: str = os.getenv("ALGORITHM", default="")


class AuthService:
    @staticmethod
    def verify_password(plain_password, hashed_password) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password):
        return pwd_context.hash(password)

    @staticmethod
    def get_user(db: DbSession, username: str):
        user: User | None = db.scalar(
            select(User).where(
                User.username == username
            )
        )
        if user:
            user_dict: dict[str, Any] = user.__dict__
            return UserInDBSchema(**user_dict)

    @staticmethod
    def authenticate_user(db: DbSession, username: str, password: str):
        user: UserInDBSchema | None = AuthService.get_user(db, username)
        if not user:
            return False
        if not AuthService.verify_password(password, user.hashed_password):
            return False
        return user

    @staticmethod
    def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
        to_encode = data.copy()
        if expires_delta:
            expire: datetime = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    @staticmethod
    async def get_current_user(db: DbSession, token: oauth_token_scheme):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username = payload.get("sub")
            if username is None:
                raise credentials_exception
            token_data = TokenData(username=username)
        except jwt.InvalidTokenError:
            raise credentials_exception
        user = AuthService.get_user(db, username=token_data.username)
        if user is None:
            raise credentials_exception
        return user

    current_user = Annotated[TokenData, Depends(get_current_user)]
