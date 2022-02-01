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

