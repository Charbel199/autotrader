from abc import ABC, ABCMeta, abstractmethod
from app.core.entities import entity_user
from typing import Dict

class AbstractTokenService(ABC):
    @abstractmethod
    async def encode_token(self, payload: Dict) -> str: raise NotImplementedError

    @abstractmethod
    async def decode_token(self, token: str) -> Dict: raise NotImplementedError
