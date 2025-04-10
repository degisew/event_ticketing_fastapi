from sqlalchemy import select
from sqlalchemy.orm import Session
from src.core.db import engine
from src.account.models import Role
from src.account.schemas.roles import BaseRoleSchema, RoleResponseSchema


class RoleService:
    @staticmethod
    def create_role(db: Session, validated_data: BaseRoleSchema):
        role = Role(
            name=validated_data.name,
            code=validated_data.code
        )

        # Add the new Role to the session
        db.add(role)
        db.commit()

        # Refresh the role object to get the ID and other DB values
        db.refresh(role)

        return role

    @staticmethod
    def list_roles():
        try:
            statement = select(Role)
            with Session(engine) as db:
                result = db.execute(statement).scalars().all()
            return [RoleResponseSchema.model_validate(role) for role in result]
        except Exception as e:
            raise e


class UserService:
    @staticmethod
    def create_user():
        pass
