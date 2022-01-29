from .interfaces.abstract_authentication_service import AbstractAuthenticationService
from .interfaces.abstract_user_service import AbstractUserService
from .interfaces.abstract_token_service import AbstractTokenService
from app.core.entities import entity_user
from app.application.exceptions.not_found_exception import NotFoundException
from app.application.exceptions.wrong_password_exception import WrongPasswordException
from app.application.exceptions.user_already_exists_exception import UserAlreadyExistsException
from passlib.hash import bcrypt


class AuthenticationService(AbstractAuthenticationService):
    def __init__(self, user_service: AbstractUserService, token_service: AbstractTokenService):
        self.user_service = user_service
        self.token_service = token_service

    async def authenticate_user(self, email: str, password: str) -> str:
        user = await self.user_service.get_user(email)
        if user.id is None:
            raise NotFoundException()
        correct_password = bcrypt.verify(password, user.hashed_password)
        if not correct_password:
            raise WrongPasswordException()
        token = await self.token_service.encode_token(entity_user.UserToken.from_orm(user).dict())
        return token

    async def register_user(self, user_data: entity_user.UserCreate) -> entity_user.UserCreateResponse:
        existing_user = await self.user_service.get_user(user_data.email)
        if existing_user.id is not None:
            raise UserAlreadyExistsException()
        user = await self.user_service.add_user(user_data)
        return user
