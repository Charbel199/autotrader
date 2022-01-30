from abc import ABC, abstractmethod
from app.core.entities import user
from app.application.models import user_model

class AbstractUserRepository(ABC):
    @abstractmethod
    async def get_user_from_email(self, email: str) -> user.User: raise NotImplementedError

    @abstractmethod
    async def add_user(self, user_data: user_model.UserCreate) -> user.User: raise NotImplementedError
