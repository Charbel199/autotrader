from .interfaces.abstract_bot_service import AbstractBotService
from app.application.models import user_model
from app.application.models import bot_model, bot_instance_model
from app.data_access.repositories.interfaces.abstract_bot_repository import AbstractBotRepository
from typing import List


class BotService(AbstractBotService):
    def __init__(self, bot_repository: AbstractBotRepository):
        self.bot_repository = bot_repository

    async def get_all_bots(self) -> List[bot_model.BotInformation]:
        bots = await self.bot_repository.get_all_bots()
        bots_to_return = [bot_model.BotInformation.from_orm(bot) for bot in bots]
        return bots_to_return

    async def get_bot_instances(self, current_user: user_model.UserToken) -> None:
        bots = await self.bot_repository.get_all_bots()

        bot_instances = await self.bot_repository.get_bot_instances(current_user.id, bots[0])
        print(vars(bot_instances[0].user))
        print("GETTING INSTANCE")

    async def add_bot_instance(self, current_user: user_model.UserToken, bot_instance: bot_instance_model.BotInstance) -> bot_instance_model.BotInstanceCreateResponse:
        pass

    async def remove_bot_instance(self, current_user: user_model.UserToken, bot_instance: bot_instance_model.BotInstance) -> None:
        pass

    async def get_bot_instance_information(self, current_user: user_model.UserToken, bot_instance: bot_instance_model.BotInstance) -> None:
        pass

    async def start_bot_instance(self, current_user: user_model.UserToken, bot_instance: bot_instance_model.BotInstance) -> None:
        pass

    async def stop_bot_instance(self, current_user: user_model.UserToken, bot_instance: bot_instance_model.BotInstance) -> None:
        pass

    async def get_bot_instance_performance(self, current_user: user_model.UserToken, bot_instance: bot_instance_model.BotInstance) -> None:
        pass

