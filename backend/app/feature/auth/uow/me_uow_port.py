from typing import Protocol
from app.feature.auth.repositories.auth_read_repository_port import (
    AuthReadRepoPort
)
from app.feature.auth.repositories.me_read_repository_port import (
    MeReadRepoPort
)
from app.feature.auth.repositories.me_update_repository_port import (
    MeUpdateRepoPort
)


class MeUoWPort(Protocol):
    me_read_repo: MeReadRepoPort
    me_update_repo: MeUpdateRepoPort
    auth_read_repo: AuthReadRepoPort
