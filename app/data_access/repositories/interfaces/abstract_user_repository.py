from abc import ABC, ABCMeta, abstractmethod
from app.data_access.persistence.models import user
from app.core.entities import entity_user

class AbstractUserRepository(ABC):
    @abstractmethod
    async def get_user_from_email(self, email: str) -> user.User: raise NotImplementedError

    @abstractmethod
    async def add_user(self, user_data: entity_user.UserCreate) -> user.User: raise NotImplementedError
