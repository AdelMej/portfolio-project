from typing import Protocol
from uuid import UUID

from app.domain.user.user_entity import AdminUserRead


class AdminUserReadRepoPort(Protocol):
    async def get_all_users(
        self,
        offset: int,
        limit: int
    ) -> tuple[list[AdminUserRead], bool]:
        ...

    async def get_user_by_id(
        self,
        user_id: UUID
    ) -> AdminUserRead | None:
        ...
