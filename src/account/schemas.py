import uuid
from pydantic import BaseModel, ConfigDict, Field, EmailStr
from src.core.schemas import BaseResponseSchema


class BaseRoleSchema(BaseModel):
    name: str = Field(max_length=10)
    code: str = Field(max_length=10)

    model_config: ConfigDict = {"from_attributes": True}


class RoleResponseSchema(BaseRoleSchema, BaseResponseSchema):
    model_config: ConfigDict = {"from_attributes": True}


class BaseUserSchema(BaseModel):
    # TODO: Remove username once it's removed from the model
    username: str
    email: EmailStr = Field(..., min_length=5, max_length=50)

    model_config: ConfigDict = {"from_attributes": True}


class UserSchema(BaseUserSchema):
    role_id: uuid.UUID
    password: str = Field(..., min_length=8, max_length=100)
    confirm_password: str = Field(..., min_length=8, max_length=100)

    model_config: ConfigDict = {"from_attributes": True}


class UserResponseSchema(BaseUserSchema, BaseResponseSchema):
    role: BaseRoleSchema
    is_active: bool
    is_profile_complete: bool

    model_config: ConfigDict = {"from_attributes": True}
