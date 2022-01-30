from .interfaces.abstract_user_service import AbstractUserService
from app.application.models import user_model
from app.data_access.repositories.interfaces.abstract_user_repository import AbstractUserRepository
from passlib.hash import bcrypt
from .interfaces.abstract_token_service import AbstractTokenService
from app.application.exceptions.wrong_password_exception import WrongPasswordException
from app.application.exceptions.not_found_exception import NotFoundException
from app.application.exceptions.user_already_exists_exception import UserAlreadyExistsException


class UserService(AbstractUserService):
    def __init__(self,
                 token_service: AbstractTokenService,
                 user_repository: AbstractUserRepository):
        self.user_repository = user_repository
        self.token_service = token_service

    async def get_user(self, email: str) -> user_model.User:
        user_from_db = await self.user_repository.get_user_from_email(email)
        user = user_model.User.from_orm(user_from_db)
        return user

    async def add_user(self, user_data: user_model.UserCreate) -> user_model.UserCreateResponse:
        user_data.password = bcrypt.hash(user_data.password)
        user_from_db = await self.user_repository.add_user(user_data)
        user = user_model.UserCreateResponse.from_orm(user_from_db)
        return user

    async def authenticate_user(self, email: str, password: str) -> str:
        # Check if user exists
        user = await self.get_user(email)
        if user.id is None:
            raise NotFoundException()
        # Compare hashed passwords
        correct_password = bcrypt.verify(password, user.hashed_password)
        if not correct_password:
            raise WrongPasswordException()
        # Generate token
        token = await self.token_service.encode_token(user_model.UserToken.from_orm(user).dict())
        return token

    async def register_user(self, user_data: user_model.UserCreate) -> user_model.UserCreateResponse:
        # Check if user exists
        existing_user = await self.get_user(user_data.email)
        if existing_user.id is not None:
            raise UserAlreadyExistsException(email=user_data.email)
        # Create new user
        user = await self.add_user(user_data)
        return user

    async def get_current_active_user(self, token: str) -> user_model.UserToken:
        payload = await self.token_service.decode_token(token)
        current_user = await self.get_user(payload['email'])
        current_user = user_model.UserToken.from_orm(current_user)
        if current_user.id is None:
            raise NotFoundException()
        return current_user
