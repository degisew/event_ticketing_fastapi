from typing import List
from fastapi import APIRouter

from src.account.schemas.roles import (
    BaseRoleSchema,
    RoleResponseSchema,
)
from src.account.services import RoleService
from src.core.db import DbSession


router = APIRouter(prefix="/roles", tags=["account"])


@router.get("/", tags=["account"])
async def get_roles() -> List[RoleResponseSchema]:
    return RoleService.list_roles()


@router.post("/", tags=["account"])
async def create_roles(session: DbSession, role: BaseRoleSchema):
    return RoleService.create_role(session, role)
