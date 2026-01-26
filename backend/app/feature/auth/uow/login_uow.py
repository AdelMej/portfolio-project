from typing import Protocol
from app.feature.auth.repositories.auth_creation_respository import (
    AuthCreationRepositoryPort
)
from app.feature.auth.repositories.auth_read_repository import (
    AuthReadRepositoryPort
)
from app.feature.auth.repositories.auth_update_repository import (
    AuthUpdateRepositoryPort
)


class LoginUoWPort(Protocol):
    auth_read: AuthReadRepositoryPort
    auth_update: AuthUpdateRepositoryPort
    auth_creation: AuthCreationRepositoryPort
