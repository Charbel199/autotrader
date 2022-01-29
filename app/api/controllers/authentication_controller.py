from fastapi import Depends, APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.core.entities import entity_user
from app.application.application_dependency_injection import Managers
from app.application.services.interfaces.abstract_authentication_service import AbstractAuthenticationService
from app.api.dependencies.user_dependency import get_current_active_user

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')
authentication_manager: AbstractAuthenticationService = Managers.authentication_manager()


@router.post("/token")
async def generate_token(form_data: OAuth2PasswordRequestForm = Depends()):
    token = await authentication_manager.authenticate_user(email=form_data.username, password=form_data.password)
    return {"access_token": token, "token_type": "bearer"}


@router.post("/register", response_model=entity_user.UserCreateResponse)
async def create_user(user_data: entity_user.UserCreate):
    return await authentication_manager.register_user(user_data)


# Test method to be removed
@router.get("/user/me", response_model=entity_user.UserToken)
async def current_user_information(current_user: entity_user.UserToken = Depends(get_current_active_user)):
    return current_user
