from pydantic import BaseModel, EmailStr, Field

from src.core.schemas import CommonResponseSchema


class BaseUserSchema(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr = Field(..., min_length=5, max_length=50)


class UserSchema(BaseUserSchema):
    password: str = Field(..., min_length=8, max_length=100)
    confirm_password: str = Field(..., min_length=8, max_length=100)


class UserResponseschema(BaseUserSchema, CommonResponseSchema):
    is_active: bool
    is_profile_complete: bool
