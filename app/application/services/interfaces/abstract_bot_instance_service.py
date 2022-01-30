from abc import ABC, abstractmethod
from app.application.models import bot_instance_model
from app.application.models import user_model
from typing import List


class AbstractBotInstanceService(ABC):
    @abstractmethod
    async def get_bot_instances(self, current_user: user_model.UserToken) -> List[bot_instance_model.BotInstance]: raise NotImplementedError

    @abstractmethod
    async def add_bot_instance(self, current_user: user_model.UserToken, bot_instance: bot_instance_model.BotInstanceCreate) -> None: raise NotImplementedError

    @abstractmethod
    async def remove_bot_instance(self, current_user: user_model.UserToken, bot_instance_id: int) -> bot_instance_model.BotInstance: raise NotImplementedError

    @abstractmethod
    async def get_bot_instance_information(self, current_user: user_model.UserToken, bot_instance_id: int) -> bot_instance_model.BotInstance: raise NotImplementedError

    # @abstractmethod
    # async def start_bot_instance(self, current_user: user_model.UserToken, bot_instance: bot_instance_model.BotInstance) -> None: raise NotImplementedError

    # @abstractmethod
    # async def stop_bot_instance(self, current_user: user_model.UserToken, bot_instance: bot_instance_model.BotInstance) -> None: raise NotImplementedError

    # @abstractmethod
    # async def get_bot_instance_performance(self, current_user: user_model.UserToken, bot_instance: bot_instance_model.BotInstance) -> None: raise NotImplementedError
