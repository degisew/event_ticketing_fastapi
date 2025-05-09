from typing import Any
from uuid import UUID

from sqlalchemy import select
from src.account.models import User
from src.core.db import DbSession


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
        try:
            result = db.scalars(select(User))
            return result
        except Exception as e:
            raise e

    @staticmethod
    def get_user_by_id(db: DbSession, user_id: UUID) -> User | None:
        user: User | None = db.get(User, user_id)

        return user
