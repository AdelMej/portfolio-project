from typing import Protocol
from app.feature.auth.repositories.auth_read_repository_port import (
    AuthReadRepositoryPort
)
from app.feature.auth.repositories.me_read_repository_port import (
    MeReadRepositoryPort
)
from app.feature.auth.repositories.me_update_repository_port import (
    MeUpdateRepositoryPort
)


class MeUoWPort(Protocol):
    me_read_repository: MeReadRepositoryPort
    me_update_repository: MeUpdateRepositoryPort
    auth_read_repository: AuthReadRepositoryPort
