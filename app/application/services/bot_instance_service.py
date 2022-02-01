from .interfaces.abstract_bot_instance_service import AbstractBotInstanceService
from app.application.models import user_model
from app.application.models import bot_model, bot_instance_model
from app.data_access.repositories.interfaces.abstract_bot_instance_repository import AbstractBotInstanceRepository
from typing import List
from app.core.entities.bot_instance import BotInstance


class BotInstanceService(AbstractBotInstanceService):

    def __init__(self, bot_instance_repository: AbstractBotInstanceRepository):
        self.bot_instance_repository = bot_instance_repository

    async def get_bot_instances(self, current_user: user_model.UserToken) -> List[bot_instance_model.BotInstance]:
        bot_instances = await self.bot_instance_repository.get_bot_instances(current_user.id)
        bot_instances_to_return = [bot_instance_model.BotInstance.from_orm(bot_instance) for bot_instance in bot_instances]
        return bot_instances_to_return

    async def add_bot_instance(self, current_user: user_model.UserToken, bot_instance: bot_instance_model.BotInstanceCreate) -> bot_instance_model.BotInstanceCreateResponse:
        bot_instance_to_add = BotInstance(**dict(bot_instance))
        bot_instance_to_add.user_id = current_user.id
        bot_instance_from_db = await self.bot_instance_repository.add_bot_instance(current_user.id, bot_instance_to_add)
        bot_instance_added = bot_instance_model.BotInstanceCreateResponse.from_orm(bot_instance_from_db)
        return bot_instance_added

    async def remove_bot_instance(self, current_user: user_model.UserToken, bot_instance_id: int) -> bot_instance_model.BotInstance:
        bot_instance_from_db = await self.bot_instance_repository.get_bot_instance(current_user.id, bot_instance_id)
        bot_instance_removed = await self.bot_instance_repository.add_bot_instance(current_user.id, bot_instance_from_db)
        bot_instance_removed_response = bot_instance_model.BotInstance.from_orm(bot_instance_removed)
        return bot_instance_removed_response

    async def get_bot_instance(self, current_user: user_model.UserToken, bot_instance_id: int) -> bot_instance_model.BotInstance:
        bot_instance_from_db = await self.bot_instance_repository.get_bot_instance(current_user.id, bot_instance_id)
        bot_instance = bot_instance_model.BotInstance.from_orm(bot_instance_from_db)
        return bot_instance
