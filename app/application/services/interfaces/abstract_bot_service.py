from abc import ABC, abstractmethod
from app.core.entities import entity_user


class AbstractBotService(ABC):
    @abstractmethod
    async def get_all_bots(self) -> str: raise NotImplementedError

    @abstractmethod
    async def get_bot_instances(self, user_data: entity_user.UserCreate) -> entity_user.UserCreateResponse: raise NotImplementedError

    @abstractmethod
    async def add_bot_instance(self, user_data: entity_user.UserCreate) -> entity_user.UserCreateResponse: raise NotImplementedError

    @abstractmethod
    async def remove_bot_instance(self, user_data: entity_user.UserCreate) -> entity_user.UserCreateResponse: raise NotImplementedError

    @abstractmethod
    async def get_bot_instance_information(self, user_data: entity_user.UserCreate) -> entity_user.UserCreateResponse: raise NotImplementedError

    @abstractmethod
    async def start_bot_instance(self, user_data: entity_user.UserCreate) -> entity_user.UserCreateResponse: raise NotImplementedError

    @abstractmethod
    async def stop_bot_instance(self, user_data: entity_user.UserCreate) -> entity_user.UserCreateResponse: raise NotImplementedError

    @abstractmethod
    async def get_bot_instance_performance(self, user_data: entity_user.UserCreate) -> entity_user.UserCreateResponse: raise NotImplementedError



