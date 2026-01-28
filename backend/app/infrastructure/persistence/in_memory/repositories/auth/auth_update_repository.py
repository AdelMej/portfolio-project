from app.domain.auth.refresh_token_entity import RefreshTokenEntity
from app.infrastructure.persistence.in_memory.storage import (
    InMemoryAuthStorage
)
from app.feature.auth.repositories.auth_update_repository import (
    AuthUpdateRepositoryPort
)
from app.shared.utils.time import utcnow


class InMemoryAuthUpdateRepository(AuthUpdateRepositoryPort):
    def __init__(self, storage: InMemoryAuthStorage) -> None:
        self._storage = storage

    async def revoke_refresh_token(self, token_hash: str) -> None:
        token = self._storage.refresh_tokens.get(token_hash)
        if not token:
            return

        self._storage.refresh_tokens[token_hash] = RefreshTokenEntity(
            user_id=token.user_id,
            token_hash=token.token_hash,
            created_at=token.created_at,
            expires_at=token.expires_at,
            revoked_at=utcnow()
        )
