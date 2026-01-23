from typing import Protocol
from uuid import UUID
from app.domain.auth.refresh_token_entity import RefreshToken


class AuthUpdateRepositoryPort(Protocol):
    async def rotate_refresh_token(self, user_id: UUID) -> RefreshToken:
        ...
