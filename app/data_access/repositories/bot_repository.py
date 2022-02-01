from typing import List

from .interfaces.abstract_bot_repository import AbstractBotRepository
from app.core.entities import user, bot, bot_instance
from app.data_access.persistence.database import Session
from sqlalchemy.orm import joinedload

# bot_instances_from_db = session.query(bot_instance.BotInstance) \
#     .options(joinedload(bot_instance.BotInstance.user)
#              .subqueryload(user.User.exchange_instances)) \
#     .filter(bot_instance.BotInstance.user_id == user_id) \
#     .all()
class BotRepository(AbstractBotRepository):

    async def get_all_bots(self) -> List[bot.Bot]:
        session = Session()
        bots_from_db = session.query(bot.Bot).all()
        session.close()
        return bots_from_db
