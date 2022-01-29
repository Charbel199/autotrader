from .interfaces.abstract_authentication_service import AbstractAuthenticationService
from .interfaces.abstract_user_service import AbstractUserService
from .interfaces.abstract_token_service import AbstractTokenService
from app.core.entities import entity_user
from app.application.exceptions.wrong_password_exception import WrongPasswordException
from app.application.exceptions.not_found_exception import NotFoundException
from app.application.exceptions.user_already_exists_exception import UserAlreadyExistsException
from passlib.hash import bcrypt


class AuthenticationService(AbstractAuthenticationService):

    def __init__(self, user_service: AbstractUserService, token_service: AbstractTokenService):
        self.user_service = user_service
        self.token_service = token_service

    async def authenticate_user(self, email: str, password: str) -> str:
        # Check if user exists
        user = await self.user_service.get_user(email)
        if user.id is None:
            raise NotFoundException()
        # Compare hashed passwords
        correct_password = bcrypt.verify(password, user.hashed_password)
        if not correct_password:
            raise WrongPasswordException()
        # Generate token
        token = await self.token_service.encode_token(entity_user.UserToken.from_orm(user).dict())
        return token

    async def register_user(self, user_data: entity_user.UserCreate) -> entity_user.UserCreateResponse:
        # Check if user exists
        existing_user = await self.user_service.get_user(user_data.email)
        if existing_user.id is not None:
            raise UserAlreadyExistsException(email=user_data.email)
        # Create new user
        user = await self.user_service.add_user(user_data)
        return user

    async def get_current_active_user(self, token: str) -> entity_user.UserToken:
        payload = await self.token_service.decode_token(token)
        current_user = await self.user_service.get_user(payload['email'])
        current_user = entity_user.UserToken.from_orm(current_user)
        if current_user.id is None:
            raise NotFoundException()
        return current_user
