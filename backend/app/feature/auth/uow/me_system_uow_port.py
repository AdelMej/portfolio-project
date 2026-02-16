from typing import Protocol

from app.feature.auth.repositories.auth_read_repository_port import (
    AuthReadRepoPort
)
from app.feature.auth.repositories.me_delete_repository_port import (
    MeDeleteRepoPort
)
from app.feature.auth.repositories.me_update_repository_port import (
    MeUpdateRepoPort
)


class MeSystemUoWPort(Protocol):
    me_update_repo: MeUpdateRepoPort
    me_delete_repo: MeDeleteRepoPort
    auth_read_repo: AuthReadRepoPort
