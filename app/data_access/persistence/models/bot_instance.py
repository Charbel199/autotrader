from sqlalchemy import Boolean, Column, Integer, String, ForeignKey

from app.data_access.persistence.base_entity import Base
from .exchange_instance import ExchangeInstance
from .bot import Bot
from .symbol_pair import SymbolPair
from .user import User


class BotInstance(Base):
    __tablename__ = "bot_instances"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    exchange_instance_id = Column(Integer, ForeignKey(ExchangeInstance.id))
    user_id = Column(Integer, ForeignKey(User.id))
    symbol_pair_id = Column(Integer, ForeignKey(SymbolPair.id))
    bot_id = Column(Integer, ForeignKey(Bot.id))
    is_on = Column(Boolean, default=False)
