from app.feature.admin.users.admin_users_service import (
    AdminUserService
)


def get_admin_user_service() -> AdminUserService:
    return AdminUserService()
