from typing import List
import uuid
from fastapi import APIRouter

from src.account.schemas.roles import (
    BaseRoleSchema,
    RoleResponseSchema,
)
from src.account.services import RoleService
from src.core.db import DbSession


router = APIRouter(prefix="/roles", tags=["account"])


@router.get("/")
async def get_roles() -> List[RoleResponseSchema]:
    return RoleService.get_roles()


@router.post("/")
async def create_roles(session: DbSession, role: BaseRoleSchema):
    return RoleService.create_role(session, role)


@router.get("/{role_id}")
async def get_role(db: DbSession, role_id: uuid.UUID) -> RoleResponseSchema:
    return RoleService.get_role(db, role_id)


@router.patch("/{role_id}")
async def update_role(db: DbSession, role_id: uuid.UUID, role: BaseRoleSchema) -> RoleResponseSchema:
    return RoleService.update_role(db, role_id, role)
