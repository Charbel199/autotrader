from abc import ABC, ABCMeta, abstractmethod
from app.data_access.persistence.models import user


class AbstractUserRepository(ABC):
    @abstractmethod
    async def get_user_from_email(self, email: str) -> user.User: raise NotImplementedError
