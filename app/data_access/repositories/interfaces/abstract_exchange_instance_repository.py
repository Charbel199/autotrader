from abc import ABC, abstractmethod
from app.core.entities import bot, exchange_instance

from typing import List


class AbstractExchangeInstanceRepository(ABC):
    @abstractmethod
    async def get_exchange_instances(self, user_id: int) -> List[exchange_instance.ExchangeInstance]: raise NotImplementedError

    @abstractmethod
    async def add_exchange_instance(self, user_id: int, exchange_instance_to_add: exchange_instance.ExchangeInstance) -> exchange_instance.ExchangeInstance: raise NotImplementedError

    @abstractmethod
    async def remove_exchange_instance(self, user_id: int, exchange_instance_to_remove: exchange_instance.ExchangeInstance) -> exchange_instance.ExchangeInstance: raise NotImplementedError

    @abstractmethod
    async def get_exchange_instance(self, user_id: int, exchange_instance_id: int) -> exchange_instance.ExchangeInstance: raise NotImplementedError
