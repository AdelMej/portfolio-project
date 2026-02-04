from typing import Protocol
from app.feature.admin.users.repositories import (
    AdminUserReadRepositoryPort,
)


class AdminUserUoWPort(Protocol):
    admin_user_read_repository: AdminUserReadRepositoryPort
