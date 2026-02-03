from uuid import UUID
from app.domain.user.user_entity import UserEntity
from typing import Protocol

from app.domain.user.user_profile_entity import UserProfileEntity


class MeReadRepositoryPort(Protocol):
    async def get(self, user_id: UUID) -> UserEntity:
        ...

    async def get_profile_by_id(self, user_id: UUID) -> UserProfileEntity:
        ...
