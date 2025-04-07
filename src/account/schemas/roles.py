from pydantic import BaseModel, Field

from src.core.schemas import CommonResponseSchema


class BaseRoleSchema(BaseModel):
    name: str = Field(max_length=10)
    code: str = Field(max_length=10)


class RoleResponseSchema(BaseRoleSchema, CommonResponseSchema):
    pass
