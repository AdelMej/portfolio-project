from typing import Protocol

from app.domain.auth.refresh_token_entity import NewRefreshTokenEntity


class AuthCreationRepositoryPort(Protocol):
    async def create_refresh_token(self, token: NewRefreshTokenEntity) -> None:
        ...
