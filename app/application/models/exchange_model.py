from typing import Optional, List
from .exchange_instance_model import ExchangeInstance
from pydantic import BaseModel, EmailStr


class ExchangeBase(BaseModel):
    exchange_name: str = None


class ExchangeInformation(ExchangeBase):
    id: int = None

    class Config:
        orm_mode = True


class Exchange(ExchangeBase):
    id: int = None
    exchange_instances: List[ExchangeInstance] = []

    class Config:
        orm_mode = True
