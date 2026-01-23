from typing import Protocol, Self
from app.feature.auth.repositories.auth_creation_respository import (
    AuthCreationRepositoryPort
)
from app.feature.auth.repositories.auth_read_repository import (
    AuthReadRepositoryPort
)

from app.feature.auth.repositories.auth_update_repository import (
    AuthUpdateRepositoryPort
)


class AuthUoW(Protocol):
    auth_read: AuthReadRepositoryPort
    auth_update: AuthUpdateRepositoryPort
    auth_creation: AuthCreationRepositoryPort

    async def __aenter__(self) -> Self: ...

    async def __aexit__(self, exc_type, exc, tb) -> None: ...
