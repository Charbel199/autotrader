from .interfaces.abstract_authentication_service import AbstractAuthenticationService
from .interfaces.abstract_user_service import AbstractUserService
from .interfaces.abstract_token_service import AbstractTokenService
from app.core.entities import entity_user
from app.application.exceptions.not_authorized_exception import NotAuthorizedException
from app.application.exceptions.not_found_exception import NotFoundException
from app.application.exceptions.wrong_password_exception import WrongPasswordException
from passlib.hash import bcrypt


class AuthenticationService(AbstractAuthenticationService):

    def __init__(self, user_service: AbstractUserService, token_service: AbstractTokenService):
        self.user_service = user_service
        self.token_service = token_service

    async def authenticate_user(self, email: str, password: str) -> str:
        user = await self.user_service.get_user(email)
        if not user:
            raise NotFoundException()
        correct_password = bcrypt.verify(password, user.hashed_password)
        if not correct_password:
            raise WrongPasswordException()
        token = await self.token_service.encode_token(user.dict())
        return token
