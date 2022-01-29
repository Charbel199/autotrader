from typing import Optional, List
from .entity_bot_instance import BotInstance
from pydantic import BaseModel, EmailStr


class BotBase(BaseModel):
    bot_name: str = None


class Bot(BotBase):
    id: int = None
    bot_instances: List[BotInstance] = []

    class Config:
        orm_mode = True
