import os
import uuid
from typing import Any
import jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status
from sqlalchemy import select
from src.account.repositories import UserRepository
from src.core.db import DbSession
from src.account.models import Role, User
from src.core.exceptions import (
    AuthenticationErrorException,
    InternalInvariantError,
    NotFoundException,
)
from src.account.schemas import (
    BaseRoleSchema,
    RoleResponseSchema,
    UserResponseSchema,
    UserSchema,
)


bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY: str = os.getenv("SECRET_KEY", default="")
ALGORITHM: str = os.getenv("ALGORITHM", default="")

if not SECRET_KEY or not ALGORITHM:
    raise InternalInvariantError(
        "Missing SECRET_KEY or ALGORITHM in .env file.")


class RoleService:
    @staticmethod
    def create_role(
        db: DbSession, validated_data: BaseRoleSchema
    ) -> RoleResponseSchema:
        serialized_data: dict[str, Any] = validated_data.model_dump(
            exclude_unset=True)
        role = Role(**serialized_data)

        db.add(role)
        db.commit()
        db.refresh(role)

        return RoleResponseSchema.model_validate(role)

    @staticmethod
    def get_roles(db: DbSession) -> list[RoleResponseSchema]:
        try:
            statement = select(Role)
            result = db.execute(statement).scalars().all()
            return [RoleResponseSchema.model_validate(role) for role in result]
        except Exception as e:
            raise e

    @staticmethod
    def get_role(db: DbSession, role_id: uuid.UUID) -> RoleResponseSchema:
        role: Role | None = db.get(Role, role_id)
        if not role:
            raise NotFoundException("Role with the given id not found.")
        return RoleResponseSchema.model_validate(role)

    @staticmethod
    def update_role(
        db: DbSession, role_id: uuid.UUID, role: BaseRoleSchema
    ) -> RoleResponseSchema:
        serialized_data: dict[str, Any] = role.model_dump(exclude_unset=True)
        role_obj: Role | None = db.get(Role, role_id)
        if role_obj is None:
            raise NotFoundException("Role with the given id not found.")

        for key, val in serialized_data.items():
            setattr(role_obj, key, val)

        db.commit()
        db.refresh(role_obj)

        return RoleResponseSchema.model_validate(role_obj)


class UserService:
    @staticmethod
    def get_password_hash(password: str) -> str:
        return bcrypt_context.hash(password)

    @staticmethod
    def create_user(
        db: DbSession,
        validated_data: UserSchema
    ) -> UserResponseSchema:
        try:
            serialized_data: dict[str, Any] = validated_data.model_dump(
                exclude_unset=True, exclude={"confirm_password"}
            )
            password = serialized_data.pop("password")

            if password != validated_data.confirm_password:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Passwords do not match.",
                )

            hashed_pass = UserService.get_password_hash(password)

            if not hashed_pass:
                raise InternalInvariantError("Password Hashing Failed.")

            serialized_data.update(password=hashed_pass)

            instance: User = UserRepository.create_user(db, serialized_data)

            return UserResponseSchema.model_validate(instance)
        except Exception as e:
            raise e

    @staticmethod
    def get_users(db: DbSession) -> list[UserResponseSchema]:
        users = UserRepository.get_users(db)

        return [UserResponseSchema.model_validate(user) for user in users]

    @staticmethod
    def get_user(db: DbSession, user_id: uuid.UUID) -> UserResponseSchema:
        user: User | None = UserRepository.get_user_by_id(db, user_id)

        if not user:
            raise NotFoundException("user with a given id not found.")

        return UserResponseSchema.model_validate(user)

    @staticmethod
    def update_user(
        db: DbSession, user_id: uuid.UUID, user: UserSchema
    ) -> UserResponseSchema:
        serialized_data: dict[str, Any] = user.model_dump(exclude_unset=True)

        user_obj: User | None = UserRepository.get_user_by_id(db, user_id)

        if not user_obj:
            raise NotFoundException("user with a given id not found.")

        updated_user = UserRepository.update_user(
            db, user_obj, serialized_data)

        return UserResponseSchema.model_validate(updated_user)

    # @staticmethod
    # def get_user_by_email(db: DbSession, email: str) -> UserResponseSchema:
    #     user: User | None = UserRepository.get_user_by_email(db, email)
    #     if not user:
    #         raise NotFoundException("User Not Found.")

    #     return UserResponseSchema.model_validate(user)

    @staticmethod
    def get_current_user(db: DbSession, token) -> UserResponseSchema:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            user_id = payload.get("user_id")
            if not user_id:
                raise AuthenticationErrorException()
        except jwt.InvalidTokenError:
            raise AuthenticationErrorException()
        user: User | None = UserRepository.get_user_by_id(db, user_id)
        if not user:
            raise AuthenticationErrorException()

        return UserResponseSchema.model_validate(user)
