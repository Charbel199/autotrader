from fastapi import Depends, APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.application.models import user_model
from app.application.application_dependency_injection import Services
from app.application.services.interfaces.abstract_user_service import AbstractUserService
from app.api.dependencies.user_dependency import get_current_active_user

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')
user_service: AbstractUserService = Services.user_service()


@router.post("/token")
async def generate_token(form_data: OAuth2PasswordRequestForm = Depends()):
    token = await user_service.authenticate_user(email=form_data.username, password=form_data.password)
    return {"access_token": token, "token_type": "bearer"}


@router.post("/register", response_model=user_model.UserCreateResponse)
async def create_user(user_data: user_model.UserCreate):
    return await user_service.register_user(user_data)


# Test method to be removed
@router.get("/user/me", response_model=user_model.UserToken)
async def current_user_information(current_user: user_model.UserToken = Depends(get_current_active_user)):
    return current_user
