from typing import Protocol
from uuid import UUID
from app.domain.session.session_entity import SessionEntity
from app.feature.session.session_dto import AttendanceOutputDto


class SessionRepository(Protocol):

    async def get_session_by_id(
        self,
        session_id: UUID
    ) -> SessionEntity | None: ...

    async def create_session(
        self,
        session: SessionEntity
    ) -> SessionEntity: ...

    async def list_sessions(
        self,
        coach_id: UUID | None = None
    ) -> list[SessionEntity]: ...

    async def update_session(
        self,
        session: SessionEntity
    ) -> SessionEntity: ...
    
    async def cancel_session(
            self, 
            session_id: UUID
    ) -> bool:
        """Returns True if updated, False if not found"""

    async def get_attendance(
            self, 
            session_id: UUID
    ) -> list[AttendanceOutputDto]: ...