from typing_extensions import Protocol

from app.feature.auth.repositories.auth_creation_respository_port import (
    AuthCreationRepoPort
)
from app.feature.auth.repositories.auth_read_repository_port import (
    AuthReadRepoPort
)
from app.feature.auth.repositories.auth_update_repository_port import (
    AuthUpdateRepoPort
)


class AuthUoWPort(Protocol):
    auth_read_repo: AuthReadRepoPort
    auth_update_repo: AuthUpdateRepoPort
    auth_creation_repo: AuthCreationRepoPort
