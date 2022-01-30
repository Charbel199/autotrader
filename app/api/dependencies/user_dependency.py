from typing import Optional
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from app.application.models import user_model
from app.application.services.interfaces.abstract_user_service import AbstractUserService
from app.application.application_dependency_injection import Services
from app.application.exceptions.not_found_exception import NotFoundException

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"token")
user_service: AbstractUserService = Services.user_service()


async def get_user_from_token(token: str = Depends(oauth2_scheme)) -> Optional[user_model.UserToken]:
    user = await user_service.get_current_active_user(token)
    return user


def get_current_active_user(current_user: user_model.UserToken = Depends(get_user_from_token)) -> Optional[user_model.UserToken]:
    if not current_user:
        raise NotFoundException()
    if not current_user.is_active:
        raise NotFoundException()
    return current_user
