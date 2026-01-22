from app.domain.session.session_creation_rules import (ensure_price_is_not_negative)
from app.feature.session.session_repository import (SessionRepository)

class SessionService:

    def __init__(self, repo: SessionRepository) -> None:
        self._repo = repo
    
    async def get_session(self):
        return{"3":"dead"}

    async def create_session(self):
        ensure_price_is_not_negative(13)
        return (self._repo.get_session_by_id)
