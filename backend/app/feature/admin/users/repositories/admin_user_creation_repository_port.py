from typing import Protocol
from uuid import UUID

from app.domain.auth.role import Role


class AdminUserCreationRepoPort(Protocol):
    async def grant_role(
        self,
        user_id: UUID,
        role: Role,
    ) -> None:
        ...
