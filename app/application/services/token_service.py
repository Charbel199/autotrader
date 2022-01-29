from typing import Dict
import jwt
from app.application.services.interfaces.abstract_token_service import AbstractTokenService
from app.core.entities import entity_user
import os
class TokenService(AbstractTokenService):
    async def encode_token(self, payload: Dict) -> str:
        return jwt.encode(payload, os.getenv("JWT_SECRET"))
