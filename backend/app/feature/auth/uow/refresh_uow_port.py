from typing import Protocol

from app.feature.auth.repositories.auth_read_repository_port import (
    AuthReadRepositoryPort
)
from app.feature.auth.repositories.auth_update_repository_port import (
    AuthUpdateRepositoryPort
)


class RefreshTokenUoWPort(Protocol):
    auth_read: AuthReadRepositoryPort
    auth_update: AuthUpdateRepositoryPort
