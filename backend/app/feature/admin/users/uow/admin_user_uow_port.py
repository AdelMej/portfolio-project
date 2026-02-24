from typing import Protocol
from app.feature.admin.users.repositories import (
    AdminUserReadRepoPort,
    AuthReadRepoPort
)


class AdminUserUoWPort(Protocol):
    admin_user_read_repo: AdminUserReadRepoPort
    auth_read_repo: AuthReadRepoPort
