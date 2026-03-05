from functools import lru_cache
from .admin_credit_service import (
    AdminCreditService
)


@lru_cache()
def get_admin_credit_service() -> AdminCreditService:
    return AdminCreditService()
