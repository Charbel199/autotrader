from abc import ABC, abstractmethod
from app.core.entities import entity_user


class AbstractUserService(ABC):
    @abstractmethod
    async def get_user(self, email: str) -> entity_user.User: raise NotImplementedError

    @abstractmethod
    async def add_user(self, user_data: entity_user.UserCreate) -> entity_user.UserCreateResponse: raise NotImplementedError

    @abstractmethod
    async def authenticate_user(self, email: str, password: str) -> str: raise NotImplementedError

    @abstractmethod
    async def register_user(self, user_data: entity_user.UserCreate) -> entity_user.UserCreateResponse: raise NotImplementedError

    @abstractmethod
    async def get_current_active_user(self, token: str) -> entity_user.UserToken: raise NotImplementedError
