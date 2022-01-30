from fastapi import APIRouter
from app.application.models import bot_model
from app.application.application_dependency_injection import Services
from app.application.services.interfaces.abstract_bot_service import AbstractBotService
from typing import List

router = APIRouter()
bot_service: AbstractBotService = Services.bot_service()


@router.get("/list", response_model=List[bot_model.BotInformation])
async def get_all_bots():
    bots = await bot_service.get_all_bots()
    return bots

