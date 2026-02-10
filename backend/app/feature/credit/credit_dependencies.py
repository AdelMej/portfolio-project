from functools import lru_cache
from .credit_service import CreditService


@lru_cache()
def get_credit_service() -> CreditService:
    return CreditService()
