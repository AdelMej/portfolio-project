from typing import Protocol

from app.feature.auth.repositories.auth_update_repository_port import (
    AuthUpdateRepositoryPort
)


class LogoutUoWPort(Protocol):
    auth_update: AuthUpdateRepositoryPort
