from typing import Protocol

from app.feature.admin.users.repositories import (
    AdminUserCreationRepoPort,
    AdminUserDeletionRepoPort,
    AdminUserUpdateRepoPort
)
from app.feature.auth.repositories.auth_read_repository_port import (
    AuthReadRepoPort
)


class AdminUserSystemUoWPort(Protocol):
    admin_user_creation_repo: AdminUserCreationRepoPort
    admin_user_update_repo: AdminUserUpdateRepoPort
    admin_user_deletion_repo: AdminUserDeletionRepoPort
    auth_read_repo: AuthReadRepoPort
