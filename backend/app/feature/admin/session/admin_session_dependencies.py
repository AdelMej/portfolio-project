from functools import lru_cache
from .admin_session_service import (
    AdminSessionService
)


@lru_cache()
def get_admin_session_service() -> AdminSessionService:
    return AdminSessionService()
