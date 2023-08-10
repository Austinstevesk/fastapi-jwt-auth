from typing import Optional

from pydantic import BaseModel, EmailStr


class BaseResponseModel(BaseModel):
    id: int

    class Config:
        from_attributes = True
        from_orm = True


class BaseInDBModel(BaseModel):
    class Config:
        from_attributes = True


class UserInDB(BaseInDBModel):
    email: EmailStr
    password: str
    name: str


class UserInResponse(BaseResponseModel):
    email: EmailStr
    name: str
    is_active: bool


class UserInLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str
    refresh_token: str


class TokenPayload(BaseModel):
    id: Optional[int]

    class Config:
        from_attributes = True
