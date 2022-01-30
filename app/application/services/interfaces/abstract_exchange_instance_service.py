from abc import ABC, abstractmethod
from app.application.models import user_model


class AbstractExchangeInstanceService(ABC):
    @abstractmethod
    async def get_exchange_instances(self, user_data: user_model.UserCreate) -> user_model.UserCreateResponse: raise NotImplementedError

    @abstractmethod
    async def add_exchange_instance(self, user_data: user_model.UserCreate) -> user_model.UserCreateResponse: raise NotImplementedError

    @abstractmethod
    async def remove_exchange_instance(self, user_data: user_model.UserCreate) -> user_model.UserCreateResponse: raise NotImplementedError

    @abstractmethod
    async def get_exchange_instance_information(self, user_data: user_model.UserCreate) -> user_model.UserCreateResponse: raise NotImplementedError



