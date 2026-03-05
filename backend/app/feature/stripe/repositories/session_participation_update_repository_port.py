from typing import Protocol
from uuid import UUID


class SessionParticipationUpdateRepoPort(Protocol):
    async def user_paid(
        self,
        session_id: UUID,
        user_id: UUID
    ) -> None:
        ...

    async def cancel_unpaid(
        self,
        session_id: UUID,
        user_id: UUID
    ) -> None:
        ...
