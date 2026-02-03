from typing import Protocol

from app.domain.user.user_entity import NewUserEntity
from app.domain.user.user_profile_entity import UserProfileEntity


class AuthCreationRepositoryPort(Protocol):
    async def register(
            self,
            user: NewUserEntity,
            user_profile: UserProfileEntity
    ) -> None:
        ...
