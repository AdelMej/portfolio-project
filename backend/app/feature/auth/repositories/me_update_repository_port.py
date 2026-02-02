from typing import Protocol
from uuid import UUID


class MeUpdateRepositoryPort(Protocol):
    async def update_email_by_user_id(self, email: str, user_id: UUID):
        ...
