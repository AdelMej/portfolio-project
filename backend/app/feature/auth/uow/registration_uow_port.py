from typing import Protocol
from app.feature.auth.repositories.auth_creation_respository_port import (
    AuthCreationRepositoryPort
)
from app.feature.auth.repositories.auth_read_repository_port import (
    AuthReadRepositoryPort
)


class RegistrationUoWPort(Protocol):
    auth_creation: AuthCreationRepositoryPort
    auth_read: AuthReadRepositoryPort
