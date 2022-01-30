from abc import ABC, abstractmethod
from app.application.models import bot_model
from typing import List


class AbstractBotService(ABC):
    @abstractmethod
    async def get_all_bots(self) -> List[bot_model.BotInformation]: raise NotImplementedError
