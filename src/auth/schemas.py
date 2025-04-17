from pydantic import BaseModel, EmailStr


class TokenSchema(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class SignInSchema(BaseModel):
    email: EmailStr
    password: str
