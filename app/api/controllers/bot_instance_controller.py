from fastapi import Depends, APIRouter
from app.application.models import user_model
from app.application.application_dependency_injection import Services
from app.application.services.interfaces.abstract_bot_instance_service import AbstractBotInstanceService
from app.api.dependencies.user_dependency import get_current_active_user
from app.application.models import bot_instance_model
from typing import List

router = APIRouter()
bot_instance_service: AbstractBotInstanceService = Services.bot_instance_service()


@router.get("/instances", response_model=List[bot_instance_model.BotInstance])
async def get_all_bot_instances(current_user: user_model.UserToken = Depends(get_current_active_user)):
    bot_instances = await bot_instance_service.get_bot_instances(current_user)
    return bot_instances


@router.post("/add", response_model=bot_instance_model.BotInstanceCreateResponse)
async def add_bot(bot_instance: bot_instance_model.BotInstanceCreate,
                  current_user: user_model.UserToken = Depends(get_current_active_user)):
    bot_instance = await bot_instance_service.add_bot_instance(current_user, bot_instance)
    return bot_instance


@router.post("/remove", response_model=bot_instance_model.BotInstance)
async def remove_bot(bot_instance_id: int,
                     current_user: user_model.UserToken = Depends(get_current_active_user)):
    bot_instance = await bot_instance_service.remove_bot_instance(current_user, bot_instance_id)
    return bot_instance


@router.get("/instance", response_model=bot_instance_model.BotInstance)
async def get_bot(bot_instance_id: int,
                  current_user: user_model.UserToken = Depends(get_current_active_user)):
    bot_instance = await bot_instance_service.get_bot_instance(current_user, bot_instance_id)
    return bot_instance
