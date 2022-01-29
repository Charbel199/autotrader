from .interfaces.abstract_user_service import AbstractUserService
from app.core.entities import entity_user
from app.data_access.repositories.interfaces.abstract_user_repository import AbstractUserRepository
from passlib.hash import bcrypt


class UserService(AbstractUserService):
    def __init__(self, user_repository: AbstractUserRepository):
        self.user_repository = user_repository

    async def get_user(self, email: str) -> entity_user.User:
        user_from_db = await self.user_repository.get_user_from_email(email)
        user = entity_user.User.from_orm(user_from_db)
        return user

    async def add_user(self, user_data: entity_user.UserCreate) -> entity_user.UserCreateResponse:
        user_data.password = bcrypt.hash(user_data.password)
        user_from_db = await self.user_repository.add_user(user_data)
        user = entity_user.UserCreateResponse.from_orm(user_from_db)
        return user
