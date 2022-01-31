from abc import ABC, abstractmethod
from typing import List
from app.application.models import exchange_model
class AbstractExchangeService(ABC):
    @abstractmethod
    async def get_all_exchanges(self) -> List[exchange_model.ExchangeInformation]: raise NotImplementedError



