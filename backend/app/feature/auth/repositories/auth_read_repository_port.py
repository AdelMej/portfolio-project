from typing import Protocol
from uuid import UUID
from app.domain.auth.refresh_token_entity import RefreshTokenEntity
from app.domain.user.user_entity import UserEntity


class AuthReadRepositoryPort(Protocol):
    async def exist_email(self, email: str) -> bool:
        ...

    async def get_user_by_email(self, email: str) -> UserEntity | None:
        ...

    async def get_refresh_token(
            self,
            token_hash: str
    ) -> RefreshTokenEntity | None:
        ...

    async def get_user_by_id(self, user_id: UUID) -> UserEntity | None:
        ...
