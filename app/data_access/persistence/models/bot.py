from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship
from app.data_access.persistence.base_entity import Base


class Bot(Base):
    __tablename__ = "bots"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    bot_name = Column(String, nullable=False)

    bot_instances = relationship("BotInstance", back_populates="bot")
