from typing import Optional, List
from .exchange_instance import ExchangeInstance
from pydantic import BaseModel, EmailStr


class ExchangeBase(BaseModel):
    exchange_name: str = None


class Exchange(ExchangeBase):
    id: int = None
    exchange_instances: List[ExchangeInstance] = []

    class Config:
        orm_mode = True
