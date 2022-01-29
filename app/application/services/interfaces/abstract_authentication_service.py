from abc import ABC, ABCMeta, abstractmethod
from app.core.entities import entity_user


class AbstractAuthenticationService(ABC):
    @abstractmethod
    async def authenticate_user(self, email: str, password: str) -> str: raise NotImplementedError
