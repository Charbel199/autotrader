from abc import ABC, abstractmethod
from app.application.models import user_model, exchange_instance_model


class AbstractExchangeInstanceService(ABC):
    @abstractmethod
    async def get_exchange_instances(self, user_data: user_model.UserToken) -> user_model.UserCreateResponse: raise NotImplementedError

    @abstractmethod
    async def add_exchange_instance(self, user_data: user_model.UserToken, exchange_instance: exchange_instance_model.ExchangeInstance) -> None: raise NotImplementedError

    @abstractmethod
    async def remove_exchange_instance(self, user_data: user_model.UserToken, exchange_instance_id: int) -> exchange_instance_model.ExchangeInstance: raise NotImplementedError

    @abstractmethod
    async def get_exchange_instance_information(self, user_data: user_model.UserToken, exchange_instance_id: int) -> exchange_instance_model.ExchangeInstance: raise NotImplementedError



