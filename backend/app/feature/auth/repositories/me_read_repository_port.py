from uuid import UUID
from app.domain.user.user_entity import UserEntity
from typing import Protocol


class MeReadRepositoryPort(Protocol):
    async def get(self, user_id: UUID) -> UserEntity:
        ...
