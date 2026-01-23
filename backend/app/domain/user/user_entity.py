from dataclasses import dataclass
from uuid import UUID
from datetime import datetime


@dataclass(frozen=True)
class UserEntity:
    id: UUID
    email: str
    password_hash: str
    disabled_at: datetime | None
    disabled_reason: str | None
