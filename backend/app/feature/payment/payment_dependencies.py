from app.feature.payment.payment_service import PaymentService
from functools import lru_cache


@lru_cache
def get_payment_service() -> PaymentService:
    return PaymentService()
