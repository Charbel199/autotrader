from abc import ABC, abstractmethod
from typing import List
from app.core.entities import exchange


class AbstractExchangeRepository(ABC):
    @abstractmethod
    async def get_all_exchanges(self) -> List[exchange.Exchange]: raise NotImplementedError
