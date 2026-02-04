from typing import Protocol

from app.domain.user.user_entity import AdminUserRead


class AdminUserReadRepositoryPort(Protocol):
    async def get_all_users(
        self,
        offset: int,
        limit: int
    ) -> tuple[list[AdminUserRead], bool]:
        ...
