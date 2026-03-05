from typing import Protocol

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
