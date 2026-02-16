from typing import Protocol
from uuid import UUID

from app.domain.auth.refresh_token_entity import NewRefreshTokenEntity


class AuthUpdateRepoPort(Protocol):
    async def revoke_refresh_token(self, token_hash: str) -> None:
        ...

    async def rotate_refresh_token(
        self,
        current_token_hash: str | None,
        new_token: NewRefreshTokenEntity
    ) -> None:
        ...

    async def revoke_all_refresh_token(self, user_id: UUID) -> None:
        ...
