from functools import lru_cache
from .admin_payment_service import (
    AdminPaymentService
)


@lru_cache()
def get_admin_payment_service() -> AdminPaymentService:
    return AdminPaymentService()
