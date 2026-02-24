from typing import Protocol
from app.feature.me.repositories.auth_read_repository_port import (
    AuthReadRepoPort
)
from app.feature.me.repositories.me_read_repository_port import (
    MeReadRepoPort
)
from app.feature.me.repositories.me_update_repository_port import (
    MeUpdateRepoPort
)


class MeUoWPort(Protocol):
    me_read_repo: MeReadRepoPort
    me_update_repo: MeUpdateRepoPort
    auth_read_repo: AuthReadRepoPort
