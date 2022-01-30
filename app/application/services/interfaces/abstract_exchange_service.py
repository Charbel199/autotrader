from abc import ABC, abstractmethod
from typing import List
from app.application.models import bot_model
class AbstractExchangeService(ABC):
    @abstractmethod
    async def get_all_exchanges(self) -> List[bot_model.BotInformation]: raise NotImplementedError



