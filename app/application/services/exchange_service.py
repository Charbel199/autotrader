from typing import List

from .interfaces.abstract_exchange_service import AbstractExchangeService
from app.application.models import user_model, exchange_model
from app.data_access.repositories.interfaces.abstract_exchange_repository import AbstractExchangeRepository


class ExchangeService(AbstractExchangeService):

    def __init__(self, exchange_repository: AbstractExchangeRepository):
        self.exchange_repository = exchange_repository

    async def get_all_exchanges(self) -> List[exchange_model.ExchangeInformation]:
        exchanges = await self.exchange_repository.get_all_exchanges()
        exchanges_to_return = [exchange_model.ExchangeInformation.from_orm(exchange) for exchange in exchanges]
        return exchanges_to_return
