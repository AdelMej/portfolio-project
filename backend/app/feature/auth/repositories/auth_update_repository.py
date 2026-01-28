from typing import Protocol


class AuthUpdateRepositoryPort(Protocol):
    async def revoke_refresh_token(self, token_hash: str) -> None:
        ...
