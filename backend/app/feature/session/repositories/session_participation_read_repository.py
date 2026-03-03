from typing import Protocol
from uuid import UUID


class SessionParticipationReadRepoPort(Protocol):
    async def has_active_participation(
        self,
        session_id: UUID,
        user_id: UUID
    ) -> bool:
        ...

    async def is_session_full(
        self,
        session_id: UUID
    ) -> bool:
        ...

    async def is_registration_open(
        self,
        session_id: UUID
    ) -> bool:
        ...

    async def get_user_registered_session_ids(
        self,
        user_id: UUID
    ) -> list[UUID]:
        ...
