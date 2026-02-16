from typing import Protocol
from app.feature.admin.users.repositories import (
    AdminUserReadRepoPort,
)


class AdminUserUoWPort(Protocol):
    admin_user_read_repo: AdminUserReadRepoPort
