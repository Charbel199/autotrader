from fastapi import APIRouter
from app.application.services.interfaces.abstract_exchange_service import AbstractExchangeService
from app.application.application_dependency_injection import Services
from typing import List
from app.application.models import exchange_model
router = APIRouter()
exchange_service: AbstractExchangeService = Services.exchange_service()


@router.get("/list", response_model=List[exchange_model.ExchangeInformation])
async def get_all_bots():
    exchanges = await exchange_service.get_all_exchanges()
    return exchanges
