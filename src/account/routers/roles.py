from typing import List
import uuid
from fastapi import APIRouter

from src.account.models import Role
from src.account.schemas import (
    BaseRoleSchema,
    RoleResponseSchema,
)
from src.account.services import RoleService
from src.core.db import DbSession


router = APIRouter(prefix="/roles", tags=["account"])


@router.get("/")
async def get_roles(db: DbSession) -> List[RoleResponseSchema]:
    return RoleService.get_roles(db)


@router.post("/")
async def create_roles(db: DbSession, role: BaseRoleSchema) -> RoleResponseSchema:
    return RoleService.create_role(db, role)


@router.get("/{role_id}")
async def get_role(db: DbSession, role_id: uuid.UUID) -> RoleResponseSchema:
    return RoleService.get_role(db, role_id)


@router.patch("/{role_id}")
async def update_role(
    db: DbSession, role_id: uuid.UUID, role: BaseRoleSchema
) -> RoleResponseSchema:
    return RoleService.update_role(db, role_id, role)
