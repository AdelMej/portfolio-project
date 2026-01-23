from app.domain.auth.refresh_token_entity import RefreshTokenEntity
from app.infrastructure.persistence.in_memory.storage import (
    InMemoryAuthStorage
)
from app.feature.auth.repositories.auth_read_repository import (
    AuthReadRepositoryPort
)


class InMemoryAuthReadRepo(AuthReadRepositoryPort):
    def __init__(self, storage: InMemoryAuthStorage) -> None:
        self._storage = storage

    async def exist_email(self, email: str) -> bool:
        return email in self._storage.users_by_email

    async def get_user_by_email(self, email: str):
        user_id = self._storage.users_by_email[email]
        return self._storage.users[user_id]

    async def get_refresh_token(self, token_hash: str) -> RefreshTokenEntity:
        return self._storage.refresh_tokens[token_hash]
