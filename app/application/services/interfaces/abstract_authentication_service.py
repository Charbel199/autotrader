from abc import ABC, abstractmethod
from app.core.entities import entity_user


class AbstractAuthenticationService(ABC):
    @abstractmethod
    async def authenticate_user(self, email: str, password: str) -> str: raise NotImplementedError

    @abstractmethod
    async def register_user(self, user_data: entity_user.UserCreate) -> entity_user.UserCreateResponse: raise NotImplementedError
