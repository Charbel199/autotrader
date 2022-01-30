from typing import Optional, List
from .bot_instance_model import BotInstance
from pydantic import BaseModel, EmailStr


class BotBase(BaseModel):
    bot_name: str = None


class BotInformation(BotBase):
    id: int = None

    class Config:
        orm_mode = True


class Bot(BotBase):
    id: int = None
    bot_instances: List[BotInstance] = []

    class Config:
        orm_mode = True
