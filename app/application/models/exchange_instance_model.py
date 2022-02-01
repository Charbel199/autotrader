from typing import Optional

from pydantic import BaseModel, EmailStr


class ExchangeInstanceBase(BaseModel):
    api_key: str = None
    api_secret: str = None


class ExchangeInstanceCreate(ExchangeInstanceBase):
    exchange_id: int = None


class ExchangeInstanceCreateResponse(ExchangeInstanceBase):
    exchange_id: int = None
    user_id: int = None

    class Config:
        orm_mode = True


class ExchangeInstance(ExchangeInstanceBase):
    id: int = None
    exchange_id: int = None
    user_id: int = None

    class Config:
        orm_mode = True
