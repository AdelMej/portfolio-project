from typing import Protocol

from app.feature.admin.users.repositories import (
    AdminUserCreationRepositoryPort,
    AdminUserDeletionRepositoryPort,
    AdminUserUpdateRepositoryPort
)


class AdminUserSystemUoWPort(Protocol):
    admin_user_creation_repository: AdminUserCreationRepositoryPort
    admin_user_update_repository: AdminUserUpdateRepositoryPort
    admin_user_deletion_repository: AdminUserDeletionRepositoryPort
