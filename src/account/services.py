from sqlalchemy.orm import Session
from sqlalchemy import select
from src.account.models import Role
from src.account.schemas.roles import BaseRoleSchema, RoleResponseSchema


class RoleService:
    @staticmethod
    def create_role(session: Session, validated_data: BaseRoleSchema):
        role = Role(
            name=validated_data.name,
            code=validated_data.code
        )

        # Add the new Role to the session
        session.add(role)
        session.commit()

        # Refresh the role object to get the ID and other DB values
        session.refresh(role)

        return role

    @staticmethod
    def list_roles(session: Session):
        stmt = select(Role)
        result = session.execute(stmt)
        roles = result.scalars().all()
        return [RoleResponseSchema.from_orm(role) for role in roles]


class UserService:
    @staticmethod
    def create_user():
        pass
