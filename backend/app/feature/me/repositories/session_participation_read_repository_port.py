from typing import Protocol
from uuid import UUID



class SessionParticipationReadRepoPort(Protocol):
    async def has_active_participation(
        self,
        session_id: UUID,
        user_id: UUID
    ) -> bool:
        ...
