from typing import Optional

from pydantic import BaseModel, EmailStr


class BotInstanceBase(BaseModel):
    is_on: bool = False


class BotInstance(BotInstanceBase):
    id: int = None
    exchange_instance_id: int = None
    user_id: int = None
    symbol_pair_id: int = None
    bot_id: int = None

    class Config:
        orm_mode = True
