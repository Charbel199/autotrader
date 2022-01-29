from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.application.services.interfaces.abstract_authentication_service import AbstractAuthenticationService
from app.core.entities import entity_user
from app.application.application_dependency_injection import Managers
from app.application.exceptions.not_found_exception import NotFoundException
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"token")
authentication_manager: AbstractAuthenticationService = Managers.authentication_manager()


async def get_user_from_token(token: str = Depends(oauth2_scheme)) -> Optional[entity_user.UserToken]:
    user = await authentication_manager.get_current_active_user(token)
    return user


def get_current_active_user(current_user: entity_user.UserToken = Depends(get_user_from_token)) -> Optional[entity_user.UserToken]:
    if not current_user:
        raise NotFoundException()
    if not current_user.is_active:
        raise NotFoundException()
    return current_user
