from dataclasses import dataclass
from uuid import UUID
from datetime import datetime

from app.domain.auth.role import Role


@dataclass(frozen=True)
class UserEntity:
    id: UUID
    email: str
    password_hash: str
    roles: set[Role]
    disabled_at: datetime | None
    disabled_reason: str | None


@dataclass(frozen=True)
class NewUserEntity:
    email: str
    password_hash: str
    role: Role


@dataclass(frozen=True)
class AdminUserRead:
    id: UUID
    email: str
    disabled_at: datetime | None
    created_at: datetime
    roles: set[Role]
