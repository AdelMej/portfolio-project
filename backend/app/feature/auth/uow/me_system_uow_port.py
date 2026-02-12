from typing import Protocol

from app.feature.auth.repositories.auth_read_repository_port import (
    AuthReadRepositoryPort
)
from app.feature.auth.repositories.me_delete_repository_port import (
    MeDeleteRepositoryPort
)
from app.feature.auth.repositories.me_update_repository_port import (
    MeUpdateRepositoryPort
)


class MeSystemUoWPort(Protocol):
    me_update_repository: MeUpdateRepositoryPort
    me_delete_repository: MeDeleteRepositoryPort
    auth_read_repository: AuthReadRepositoryPort
