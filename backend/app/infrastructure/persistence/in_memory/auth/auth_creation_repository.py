from app.domain.auth.refresh_token_entity import (
    NewRefreshTokenEntity,
    RefreshTokenEntity
)
from app.infrastructure.persistence.in_memory.storage import (
    InMemoryAuthStorage
)
from app.feature.auth.repositories.auth_creation_respository import (
    AuthCreationRepositoryPort
)
from app.shared.utils.time import utcnow


class InMemoryAuthCreationRepository(AuthCreationRepositoryPort):
    def __init__(self, storage: InMemoryAuthStorage) -> None:
        self._storage = storage

    async def create_refresh_token(self, token: NewRefreshTokenEntity) -> None:
        self._storage.refresh_tokens[token.token_hash] = RefreshTokenEntity(
            user_id=token.user_id,
            token_hash=token.token_hash,
            created_at=utcnow(),
            expires_at=token.expires_at,
            revoked_at=None
        )
