from pydantic import BaseModel, Field, EmailStr
from src.core.schemas import CommonResponseSchema


class BaseRoleSchema(BaseModel):
    name: str = Field(max_length=10)
    code: str = Field(max_length=10)


class RoleResponseSchema(BaseRoleSchema, CommonResponseSchema):
    class Config:
        from_attributes = True  # needed to use model_validate method in the service


class BaseUserSchema(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr = Field(..., min_length=5, max_length=50)


class UserSchema(BaseUserSchema):
    password: str = Field(..., min_length=8, max_length=100)
    confirm_password: str = Field(..., min_length=8, max_length=100)


class UserResponseSchema(BaseUserSchema, CommonResponseSchema):
    is_active: bool
    is_profile_complete: bool

    class Config:
        from_attributes = True
