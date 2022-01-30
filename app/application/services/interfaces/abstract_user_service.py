from abc import ABC, abstractmethod
from app.application.models import user_model


class AbstractUserService(ABC):
    @abstractmethod
    async def get_user(self, email: str) -> user_model.User: raise NotImplementedError

    @abstractmethod
    async def add_user(self, user_data: user_model.UserCreate) -> user_model.UserCreateResponse: raise NotImplementedError

    @abstractmethod
    async def authenticate_user(self, email: str, password: str) -> str: raise NotImplementedError

    @abstractmethod
    async def register_user(self, user_data: user_model.UserCreate) -> user_model.UserCreateResponse: raise NotImplementedError

    @abstractmethod
    async def get_current_active_user(self, token: str) -> user_model.UserToken: raise NotImplementedError
