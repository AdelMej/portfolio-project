from functools import lru_cache
from app.feature.admin.users.admin_users_service import (
    AdminUserService
)


@lru_cache()
def get_admin_user_service() -> AdminUserService:
    return AdminUserService()
