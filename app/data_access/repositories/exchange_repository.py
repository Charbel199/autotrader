from typing import List

from .interfaces.abstract_exchange_repository import AbstractExchangeRepository
from app.core.entities import user, bot, bot_instance, exchange
from app.data_access.persistence.database import Session
from sqlalchemy.orm import joinedload


class ExchangeRepository(AbstractExchangeRepository):

    async def get_all_exchanges(self) -> List[exchange.Exchange]:
        session = Session()
        exchanges_from_db = session.query(exchange.Exchange).all()
        session.close()
        return exchanges_from_db

