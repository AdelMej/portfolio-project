from typing import Protocol

class SessionRepository(Protocol):
    async def get_session_by_id(): ...