from abc import ABC, abstractmethod
from app.core.entities import bot, bot_instance

from typing import List


class AbstractBotRepository(ABC):
    @abstractmethod
    async def get_all_bots(self) -> List[bot.Bot]: raise NotImplementedError
