from datetime import datetime
from typing import Protocol
from uuid import UUID


class SessionUpdateRepoPort(Protocol):

    async def update_session(
        self,
        session_id: UUID,
        title: str,
        starts_at: datetime,
        ends_at: datetime
    ) -> None:
        ...

    async def cancel_session(
            self,
            session_id: UUID
    ) -> None:
        ...
