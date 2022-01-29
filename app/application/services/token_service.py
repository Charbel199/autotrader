from typing import Dict
import jwt
from app.application.services.interfaces.abstract_token_service import AbstractTokenService
import os


class TokenService(AbstractTokenService):
    async def decode_token(self, token: str) -> Dict:
        return jwt.decode(token, os.getenv("JWT_SECRET"), algorithms=["HS256"])

    async def encode_token(self, payload: Dict) -> str:
        return jwt.encode(payload, os.getenv("JWT_SECRET"), algorithm="HS256")
