from typing import Protocol
from uuid import UUID


class AuthUpdateRepoPort(Protocol):
    async def revoke_all_refresh_token(self, user_id: UUID) -> None:
        ...
