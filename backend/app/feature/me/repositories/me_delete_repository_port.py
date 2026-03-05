from typing import Protocol
from uuid import UUID


class MeDeleteRepoPort(Protocol):
    async def soft_delete_user(
            self,
            user_id: UUID,
    ) -> None:
        ...
