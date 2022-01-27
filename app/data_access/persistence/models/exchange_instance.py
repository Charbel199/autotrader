from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.data_access.persistence.base_entity import Base
from .exchange import Exchange
from .user import User

class ExchangeInstance(Base):
    __tablename__ = "exchange_instances"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    exchange_id = Column(Integer, ForeignKey(Exchange.id))
    user_id = Column(Integer, ForeignKey(User.id))
    api_key = Column(String)
    api_secret = Column(String)

    exchange = relationship("Exchange", back_populates="exchange_instances")
    user = relationship("User", back_populates="exchange_instances")
    bot_instances = relationship("BotInstances", back_populates="exchange_instance")
