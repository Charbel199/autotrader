from fastapi import Depends, APIRouter
from app.application.models import user_model
from app.application.application_dependency_injection import Services
from app.application.services.interfaces.abstract_bot_service import AbstractBotService
from app.api.dependencies.user_dependency import get_current_active_user

router = APIRouter()
bot_service: AbstractBotService = Services.bot_service()

@router.get("/instances")
async def get_all_bots(current_user: user_model.UserToken = Depends(get_current_active_user)):
    await bot_service.get_bot_instances(current_user)
    return {"GOOD": "GOOD"}
