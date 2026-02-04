from typing_extensions import Protocol

from app.feature.auth.repositories.auth_creation_respository_port import (
    AuthCreationRepositoryPort
)
from app.feature.auth.repositories.auth_read_repository_port import (
    AuthReadRepositoryPort
)
from app.feature.auth.repositories.auth_update_repository_port import (
    AuthUpdateRepositoryPort
)


class AuthUoWPort(Protocol):
    auth_read_repository: AuthReadRepositoryPort
    auth_update_repository: AuthUpdateRepositoryPort
    auth_creation_repository: AuthCreationRepositoryPort
