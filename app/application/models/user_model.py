from typing import Optional

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: EmailStr = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class UserCreate(UserBase):
    password: str = None


class UserCreateResponse(UserBase):
    id: int = None
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class UserToken(UserBase):
    id: int = None
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class User(UserBase):
    id: int = None
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False
    hashed_password: str = None

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
