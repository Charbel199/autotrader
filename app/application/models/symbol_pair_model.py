from typing import Optional, List
from .bot_instance_model import BotInstance
from pydantic import BaseModel, EmailStr


class SymbolPairBase(BaseModel):
    primary_symbol: str = None
    secondary_symbol: str = None


class SymbolPair(SymbolPairBase):
    id: int = None
    bot_instances: List[BotInstance] = []

    class Config:
        orm_mode = True
