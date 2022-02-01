from typing import List

from .interfaces.abstract_bot_instance_repository import AbstractBotInstanceRepository
from app.core.entities import user, bot, bot_instance, exchange, exchange_instance
from app.data_access.persistence.database import Session


class BotInstanceRepository(AbstractBotInstanceRepository):

    async def get_bot_instances(self, user_id: int) -> List[bot_instance.BotInstance]:
        session = Session()
        bot_instances_from_db = session.query(bot_instance.BotInstance).filter(user.User.id == user_id).all()
        session.close()
        return bot_instances_from_db

    async def add_bot_instance(self, user_id: int, bot_instance_to_add: bot_instance.BotInstance) -> bot_instance.BotInstance:
        session = Session()
        session.add(bot_instance_to_add)
        session.commit()
        session.refresh(bot_instance_to_add)
        session.close()
        return bot_instance_to_add

    async def remove_bot_instance(self, user_id: int, bot_instance_to_remove: bot_instance.BotInstance) -> bot_instance.BotInstance:
        session = Session()
        session.delete(bot_instance_to_remove)
        session.commit()
        session.close()
        return bot_instance_to_remove

    async def get_bot_instance(self, user_id: int, bot_instance_id: int) -> bot_instance.BotInstance:
        session = Session()
        bot_instance_from_db = session.query(bot_instance.BotInstance).filter(bot_instance.BotInstance.id == bot_instance_id).first()
        session.close()
        return bot_instance_from_db
