from typing import Protocol
from app.feature.auth.repositories.auth_creation_respository_port import (
    AuthCreationRepoPort
)
from app.feature.auth.repositories.auth_read_repository_port import (
    AuthReadRepoPort
)


class RegistrationUoWPort(Protocol):
    auth_creation_repo: AuthCreationRepoPort
    auth_read_repo: AuthReadRepoPort
