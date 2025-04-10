import uuid
from src.core.exceptions import NotFoundException
from sqlalchemy import select
from sqlalchemy.orm import Session
from src.core.db import engine
from src.account.models import Role
from src.account.schemas.roles import BaseRoleSchema, RoleResponseSchema


class RoleService:
    @staticmethod
    def create_role(db: Session, validated_data: BaseRoleSchema):
        role = Role(name=validated_data.name, code=validated_data.code)

        # Add the new Role to the session
        db.add(role)
        db.commit()

        # Refresh the role object to get the ID and other DB values
        db.refresh(role)

        return role

    @staticmethod
    def get_roles() -> list[RoleResponseSchema]:
        try:
            statement = select(Role)
            with Session(engine) as db:
                result = db.execute(statement).scalars().all()
            return [RoleResponseSchema.model_validate(role) for role in result]
        except Exception as e:
            raise e

    @staticmethod
    def get_role(db: Session, role_id: uuid.UUID) -> RoleResponseSchema:
        role = db.get(Role, role_id)
        if not role:
            raise NotFoundException("Role with the given id not found.")
        return RoleResponseSchema.model_validate(role)
        # TODO: check the differenceb/n this and the comented code below
        # stmt = select(Role).where(Role.id == role_id)
        # with Session(engine) as db:
        #     result = db.execute(stmt).scalars().first()
        # if not result:
        #     raise NotFoundException("Role with the given id not found.")
        # return RoleResponseSchema.model_validate(result)

    @staticmethod
    def update_role(
        db: Session, role_id: uuid.UUID, role: BaseRoleSchema
    ) -> RoleResponseSchema:
        role_obj = db.get(Role, role_id)
        if role_obj is None:
            raise NotFoundException("Role with the given id not found.")

        for key, val in role.model_dump(exclude_unset=True).items():
            setattr(role_obj, key, val)

        db.commit()
        db.refresh(role_obj)

        return RoleResponseSchema.model_validate(role_obj)


class UserService:
    @staticmethod
    def create_user():
        pass
