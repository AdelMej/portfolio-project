from typing import Protocol
from uuid import UUID


class AdminSessionUpdateRepoPort(Protocol):
    async def cancel_session(
            self,
            session_id: UUID
    ) -> None:
        ...
