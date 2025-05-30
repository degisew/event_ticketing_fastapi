from uuid import UUID
from typing import Any
from sqlalchemy import select, update
from sqlalchemy.exc import SQLAlchemyError, NoResultFound
from src.account.models import Role, User
from src.core.db import DbSession
from src.core.logger import logger


class RoleRepository:
    @staticmethod
    def create_role(db: DbSession, serialized_data: dict[str, Any]) -> Role:
        instance = Role(**serialized_data)
        db.add(instance)
        db.commit()

        db.refresh(instance)

        return instance

    @staticmethod
    def get_role_by_id(db: DbSession, role_id: UUID) -> Role | None:
        role: Role | None = db.get(Role, role_id)

        return role

    @staticmethod
    def get_roles(db: DbSession):
        result = db.scalars(select(Role))
        return result

    @staticmethod
    def update_role(db: DbSession, role_obj, serialized_data: dict[str, Any]):
        for key, val in serialized_data.items():
            if getattr(role_obj, key) != val:
                setattr(role_obj, key, val)

        db.commit()
        db.refresh(role_obj)

        return role_obj


class UserRepository:
    @staticmethod
    def create_user(db: DbSession, serialized_data: dict[str, Any]) -> User:
        instance = User(**serialized_data)

        db.add(instance)

        db.commit()

        db.refresh(instance)

        return instance

    @staticmethod
    def get_users(db: DbSession):
        result = db.scalars(select(User))
        return result

    @staticmethod
    def get_user_by_id(db: DbSession, user_id: UUID) -> User | None:
        user: User | None = db.get(User, user_id)

        return user

    @staticmethod
    def update_user(db: DbSession, user_obj, serialized_data: dict[str, Any]):
        for key, val in serialized_data.items():
            if getattr(user_obj, key) != val:  # * Prevent unnecessary DB writes
                setattr(user_obj, key, val)

        db.commit()
        db.refresh(user_obj)

        return user_obj

    @staticmethod
    def get_user_by_email(db: DbSession, email: str):
        user: User | None = db.scalar(select(User).where(User.email == email))

        return user
