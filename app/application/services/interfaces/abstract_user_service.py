from abc import ABC, ABCMeta, abstractmethod
from app.core.entities import entity_user


class AbstractUserService(ABC):
    @abstractmethod
    async def get_user(self, email: str) -> entity_user.User: raise NotImplementedError
