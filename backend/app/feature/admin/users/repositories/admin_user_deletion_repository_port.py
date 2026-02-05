from typing import Protocol
from uuid import UUID

from app.domain.auth.role import Role


class AdminUserDeletionRepositoryPort(Protocol):
    async def revoke_role(
        self,
        user_id: UUID,
        role: Role
    ) -> None:
        ...
