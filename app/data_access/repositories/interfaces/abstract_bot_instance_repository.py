from abc import ABC, abstractmethod
from app.core.entities import bot, bot_instance

from typing import List


class AbstractBotInstanceRepository(ABC):
    @abstractmethod
    async def get_bot_instances(self, user_id: int) -> List[bot_instance.BotInstance]: raise NotImplementedError

    @abstractmethod
    async def add_bot_instance(self, user_id: int, bot_instance_to_add: bot_instance.BotInstance) -> bot_instance.BotInstance: raise NotImplementedError

    @abstractmethod
    async def remove_bot_instance(self, user_id: int, bot_instance_to_remove: bot_instance.BotInstance) -> bot_instance.BotInstance: raise NotImplementedError

    @abstractmethod
    async def get_bot_instance(self, user_id: int, bot_instance_id: int) -> bot_instance.BotInstance: raise NotImplementedError
