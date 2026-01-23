from dataclasses import dataclass
from datetime import datetime, timezone
from uuid import UUID


@dataclass(frozen=True)
class RefreshToken:
    id: UUID
    user_id: UUID
    token_hash: str
    created_at: datetime                # must be tz-aware UTC
    expires_at: datetime                # must be tz-aware UTC
    revoked_at: datetime | None
    replaced_by_token_id: UUID | None

    def is_revoked(self) -> bool:
        return self.revoked_at is not None

    def is_expired(self, *, now: datetime | None = None) -> bool:
        now = now or datetime.now(timezone.utc)
        return self.expires_at <= now

    def is_active(self, *, now: datetime | None = None) -> bool:
        return not self.is_revoked() and not self.is_expired(now=now)
