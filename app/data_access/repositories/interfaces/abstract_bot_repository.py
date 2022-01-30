from abc import ABC, abstractmethod
from app.core.entities import bot, bot_instance

from typing import List


class AbstractBotRepository(ABC):
    @abstractmethod
    async def get_all_bots(self) -> List[bot.Bot]: raise NotImplementedError

    @abstractmethod
    async def get_bot_instances(self, user_id: int, bot: bot.Bot) -> List[bot_instance.BotInstance]: raise NotImplementedError
