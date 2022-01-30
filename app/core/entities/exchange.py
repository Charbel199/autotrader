from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship
from app.data_access.persistence.base_entity import Base


class Exchange(Base):
    __tablename__ = "exchanges"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    exchange_name = Column(String, nullable=False)

    exchange_instances = relationship("ExchangeInstance", back_populates="exchange")