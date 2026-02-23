from datetime import datetime
from typing import Protocol
from uuid import UUID

from app.domain.session.session_entity import (
    SessionEntity,
    SessionWithCoachEntity
)


class SessionReadRepoPort(Protocol):
    async def get_session_by_id(
        self,
        session_id: UUID
    ) -> SessionWithCoachEntity:
        ...

    async def get_all_sessions(
        self,
        offset: int,
        limit: int,
        _from: datetime | None,
        to: datetime | None
    ) -> tuple[list[SessionWithCoachEntity], bool]:
        ...

    async def is_session_overlapping(
        self,
        starts_at: datetime,
        ends_at: datetime
    ) -> bool:
        ...

    async def is_session_overlapping_except(
        self,
        starts_at: datetime,
        ends_at: datetime,
        except_session_id: UUID
    ) -> bool:
        ...

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

    async def is_session_started(
        self,
        session_id: UUID
    ) -> bool:
        ...

    async def system_get_session_by_id(
        self,
        session_id: UUID
    ) -> SessionEntity:
        ...

    async def public_exists_session(
        self,
        session_id: UUID
    ) -> bool:
        ...
