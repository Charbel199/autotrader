from .interfaces.abstract_user_service import AbstractUserService
from app.core.entities import entity_user
from app.data_access.repositories.interfaces.abstract_user_repository import AbstractUserRepository


class UserService(AbstractUserService):
    def __init__(self, user_repository: AbstractUserRepository):
        self.user_repository = user_repository

    async def get_user(self, email: str) -> entity_user.User:
        user_from_db = self.user_repository.get_user_from_email(email)
        user = entity_user.User.from_orm(user_from_db)
        return user
