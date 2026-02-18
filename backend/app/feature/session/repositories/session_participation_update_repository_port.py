from typing import Protocol
from uuid import UUID


class SessionParticipationUpdateRepoPort(Protocol):
    async def cancel_registration(
        self,
        user_id: UUID,
        session_id: UUID
    ) -> None:
        ...
