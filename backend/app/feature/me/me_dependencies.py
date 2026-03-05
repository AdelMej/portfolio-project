from functools import lru_cache
from app.feature.me.me_service import (
    MeService
)


@lru_cache()
def get_me_service() -> MeService:
    return MeService()
