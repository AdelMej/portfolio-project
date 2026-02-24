from typing import Protocol

from app.feature.me.repositories.auth_read_repository_port import (
    AuthReadRepoPort
)
from app.feature.me.repositories.auth_update_repo_port import (
    AuthUpdateRepoPort
)
from app.feature.me.repositories.me_delete_repository_port import (
    MeDeleteRepoPort
)
from app.feature.me.repositories.me_update_repository_port import (
    MeUpdateRepoPort
)


class MeSystemUoWPort(Protocol):
    me_update_repo: MeUpdateRepoPort
    me_delete_repo: MeDeleteRepoPort
    auth_read_repo: AuthReadRepoPort
    auth_update_repo: AuthUpdateRepoPort
