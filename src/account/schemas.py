import uuid
from pydantic import BaseModel, EmailStr, Field


class UserSchema(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr = Field(..., min_length=5, max_length=50)
    password: str = Field(..., min_length=8, max_length=100)
    confirm_password: str = Field(..., min_length=8, max_length=100)


class UserResponseschema(BaseModel):
    id: uuid.UUID
    username: str
    email: EmailStr
    is_active: bool
    is_profile_complete: bool
    created_at: str
    updated_at: str
