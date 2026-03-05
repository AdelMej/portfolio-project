from functools import lru_cache
from .coach_service import CoachService


@lru_cache()
def get_coach_service() -> CoachService:
    return CoachService()
