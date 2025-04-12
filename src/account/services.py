import uuid
from typing import Any
from sqlalchemy import select
from src.core.db import DbSession
from src.account.models import Role, User
from src.core.exceptions import NotFoundException
from src.account.schemas import (
    BaseRoleSchema,
    RoleResponseSchema,
    UserResponseSchema,
    UserSchema,
)


class RoleService:
    @staticmethod
    def create_role(
        db: DbSession, validated_data: BaseRoleSchema
    ) -> RoleResponseSchema:
        serialized_data: dict[str, Any] = validated_data.model_dump(exclude_unset=True)
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
    def create_user(db: DbSession, validated_data: UserSchema) -> UserResponseSchema:
        serialized_data: dict[str, Any] = validated_data.model_dump(
            exclude_unset=True, exclude={"confirm_password"}
        )
        instance = User(**serialized_data)

        db.add(instance)

        db.commit()

        db.refresh(instance)

        return UserResponseSchema.model_validate(instance)

    @staticmethod
    def get_users(db: DbSession) -> list[UserResponseSchema]:
        try:
            stmt = select(User)
            result = db.execute(stmt).scalars().all()

            return [UserResponseSchema.model_validate(user) for user in result]
        except Exception as e:
            raise e

    @staticmethod
    def get_user(db: DbSession, user_id: uuid.UUID) -> UserResponseSchema:
        user: User | None = db.get(User, user_id)

        if not user:
            raise NotFoundException("user with a given id not found.")

        return UserResponseSchema.model_validate(user)

    @staticmethod
    def update_user(
        db: DbSession, user_id: uuid.UUID, user: UserSchema
    ) -> UserResponseSchema:
        serialized_data = user.model_dump(exclude_unset=True)
        user_obj = db.get(User, user_id)

        if not user_obj:
            raise NotFoundException("user with a given id not found.")
        for key, val in serialized_data.items():
            if getattr(user_obj, key) != val:  # * Prevent unnecessary DB writes
                setattr(user_obj, key, val)

        db.commit()
        db.refresh(user_obj)

        return UserResponseSchema.model_validate(user_obj)
