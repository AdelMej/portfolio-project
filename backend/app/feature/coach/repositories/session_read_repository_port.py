from typing import Protocol
from uuid import UUID


class SessionReadRepoPort(Protocol):
    async def exist_session(
        self,
        session_id: UUID
    ) -> bool:
        ...

    async def is_session_owner(
        self,
        session_id: UUID,
        user_id: UUID
    ) -> bool:
        ...

    async def is_session_cancelled(
        self,
        session_id: UUID
    ) -> bool:
        ...

    async def is_session_finished(
        self,
        session_id: UUID
    ) -> bool:
        ...
