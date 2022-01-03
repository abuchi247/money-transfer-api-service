from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from enum import Enum


class Role(str, Enum):
    ADMIN: str = "admin"
    REGULAR: str = "regular"


class UserBase(BaseModel):
    email: EmailStr  # email validation


class UserCreate(UserBase):
    password: str


class UserLogin(UserCreate):
    pass


# Schema for response
class User(UserBase):
    id: int
    # role: Role = Field(exclude=True)
    created_at: datetime

    class Config:
        orm_mode = True
        # use_enum_values = True


class UserOut(UserBase):
    id: int

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None
