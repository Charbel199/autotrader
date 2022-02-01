from fastapi import Depends, APIRouter
from app.application.models import user_model
from app.application.application_dependency_injection import Services
from app.application.services.interfaces.abstract_exchange_instance_service import AbstractExchangeInstanceService
from app.api.dependencies.user_dependency import get_current_active_user
from app.application.models import exchange_instance_model
from typing import List

router = APIRouter()
exchange_instance_service: AbstractExchangeInstanceService = Services.exchange_instance_service()


@router.get("/instances", response_model=List[exchange_instance_model.ExchangeInstance])
async def get_all_exchange_instances(current_user: user_model.UserToken = Depends(get_current_active_user)):
    exchange_instances = await exchange_instance_service.get_exchange_instances(current_user)
    return exchange_instances


@router.post("/add", response_model=exchange_instance_model.ExchangeInstanceCreateResponse)
async def add_exchange(exchange_instance: exchange_instance_model.ExchangeInstanceCreate,
                       current_user: user_model.UserToken = Depends(get_current_active_user)):
    exchange_instance = await exchange_instance_service.add_exchange_instance(current_user, exchange_instance)
    return exchange_instance


@router.post("/remove", response_model=exchange_instance_model.ExchangeInstance)
async def remove_exchange(exchange_instance_id: int,
                          current_user: user_model.UserToken = Depends(get_current_active_user)):
    exchange_instance = await exchange_instance_service.remove_exchange_instance(current_user, exchange_instance_id)
    return exchange_instance


@router.get("/instance", response_model=exchange_instance_model.ExchangeInstance)
async def get_exchange(exchange_instance_id: int,
                       current_user: user_model.UserToken = Depends(get_current_active_user)):
    exchange_instance = await exchange_instance_service.get_exchange_instance(current_user, exchange_instance_id)
    return exchange_instance
