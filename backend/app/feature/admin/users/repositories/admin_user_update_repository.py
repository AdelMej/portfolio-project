from typing import Protocol
from uuid import UUID


class AdminUserUpdateRepositoryPort(Protocol):
    async def disable_user(
        self,
        user_id: UUID
    ) -> None:
        ...

    async def reenable_user(
        self,
        user_id: UUID
    ) -> None:
        ...
