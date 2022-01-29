from abc import ABC, abstractmethod
from app.core.entities import entity_user


class AbstractExchangeService(ABC):
    @abstractmethod
    async def get_all_exchanges(self) -> str: raise NotImplementedError

    @abstractmethod
    async def get_exchange_instances(self, user_data: entity_user.UserCreate) -> entity_user.UserCreateResponse: raise NotImplementedError

    @abstractmethod
    async def add_exchange_instance(self, user_data: entity_user.UserCreate) -> entity_user.UserCreateResponse: raise NotImplementedError

    @abstractmethod
    async def remove_exchange_instance(self, user_data: entity_user.UserCreate) -> entity_user.UserCreateResponse: raise NotImplementedError

    @abstractmethod
    async def get_exchange_instance_information(self, user_data: entity_user.UserCreate) -> entity_user.UserCreateResponse: raise NotImplementedError



