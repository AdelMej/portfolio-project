from functools import lru_cache
from .stripe_service import StripeService


@lru_cache()
def get_stripe_service() -> StripeService:
    return StripeService()
