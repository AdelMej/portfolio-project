from typing import Protocol
from uuid import UUID

from app.domain.user.user_entity import UserEntity


class AuthReadRepoPort(Protocol):
    async def is_user_disabled(
        self,
        user_id
    ) -> bool:
        ...

    async def exist_email(self, email: str) -> bool:
        ...

    async def get_user_by_id(
        self,
        user_id: UUID
    ) -> UserEntity:
        ...
