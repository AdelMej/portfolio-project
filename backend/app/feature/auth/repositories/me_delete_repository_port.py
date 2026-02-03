from typing import Protocol
from uuid import UUID


class MeDeleteRepositoryPort(Protocol):
    async def soft_delete_user(
            self,
            user_id: UUID,
            new_password_hash: str
    ) -> None:
        ...
