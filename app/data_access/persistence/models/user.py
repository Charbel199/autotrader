from sqlalchemy import Boolean, Column, Integer, String
from app.data_access.persistence.base_entity import Base
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    first_name = Column(String)
    last_name = Column(String)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    is_verified = Column(Boolean, default=False)

    exchange_instances = relationship("ExchangeInstance", back_populates="user")
    bot_instances = relationship("BotInstance", back_populates="user")
