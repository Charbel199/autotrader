from abc import ABC, abstractmethod
from app.application.models import user_model, exchange_instance_model
from typing import List

class AbstractExchangeInstanceService(ABC):
    @abstractmethod
    async def get_exchange_instances(self, current_user: user_model.UserToken) -> List[exchange_instance_model.ExchangeInstance]: raise NotImplementedError

    @abstractmethod
    async def add_exchange_instance(self, current_user: user_model.UserToken, exchange_instance: exchange_instance_model.ExchangeInstanceCreate) -> exchange_instance_model.ExchangeInstanceCreateResponse: raise NotImplementedError

    @abstractmethod
    async def remove_exchange_instance(self, current_user: user_model.UserToken, exchange_instance_id: int) -> exchange_instance_model.ExchangeInstance: raise NotImplementedError

    @abstractmethod
    async def get_exchange_instance(self, current_user: user_model.UserToken, exchange_instance_id: int) -> exchange_instance_model.ExchangeInstance: raise NotImplementedError



