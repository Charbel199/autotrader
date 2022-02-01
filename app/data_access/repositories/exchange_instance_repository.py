from typing import List

from .interfaces.abstract_exchange_instance_repository import AbstractExchangeInstanceRepository
from app.core.entities import user, bot, bot_instance, exchange, exchange_instance
from app.data_access.persistence.database import Session


class ExchangeInstanceRepository(AbstractExchangeInstanceRepository):

    async def get_exchange_instances(self, user_id: int) -> List[exchange_instance.ExchangeInstance]:
        session = Session()
        exchange_instances_from_db = session.query(exchange_instance.ExchangeInstance).filter(user.User.id == user_id).all()
        session.close()
        return exchange_instances_from_db

    async def add_exchange_instance(self, user_id: int, exchange_instance_to_add: exchange_instance.ExchangeInstance) -> exchange_instance.ExchangeInstance:
        session = Session()
        session.add(exchange_instance_to_add)
        session.commit()
        session.refresh(exchange_instance_to_add)
        session.close()
        return exchange_instance_to_add

    async def remove_exchange_instance(self, user_id: int, exchange_instance_to_remove: exchange_instance.ExchangeInstance) -> exchange_instance.ExchangeInstance:
        session = Session()
        session.delete(exchange_instance_to_remove)
        session.commit()
        session.close()
        return exchange_instance_to_remove

    async def get_exchange_instance(self, user_id: int, exchange_instance_id: int) -> exchange_instance.ExchangeInstance:
        session = Session()
        exchange_instance_from_db = session.query(exchange_instance.ExchangeInstance).filter(exchange_instance.ExchangeInstance.id == exchange_instance_id).first()
        session.close()
        return exchange_instance_from_db
