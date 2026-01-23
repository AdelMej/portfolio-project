from uuid import uuid4
from datetime import datetime, timedelta, timezone
from app.domain.auth.refresh_token_entity import RefreshToken
from app.infrastructure.persistence.in_memory.storage import (
    InMemoryAuthStorage
)


class InMemoryAuthUpdateRepo:
    def __init__(self, storage: InMemoryAuthStorage) -> None:
        self._storage = storage

    async def rotate_refresh_token(self, user_id):
        now = datetime.now(timezone.utc)

        token = RefreshToken(
            id=uuid4(),
            user_id=user_id,
            token_hash="fake-hash",
            created_at=now,
            expires_at=now + timedelta(days=30),
            revoked_at=None,
            replaced_by_token_id=None,
        )

        self._storage.refresh_tokens[token.id] = token
        return token
