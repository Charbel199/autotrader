from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship
from app.data_access.persistence.base_entity import Base


class SymbolPair(Base):
    __tablename__ = "symbol_pairs"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    primary_symbol = Column(String, nullable=False)
    secondary_symbol = Column(String, nullable=False)

    bot_instances = relationship("BotInstances", back_populates="symbol_pair")
