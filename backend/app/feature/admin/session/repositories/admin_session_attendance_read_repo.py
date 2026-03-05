from typing import Protocol
from uuid import UUID

from app.domain.user.user_profile_entity import AdminUserAttendanceRead


class AdminSessionAttendanceReadRepoPort(Protocol):
    async def get_session_attendance_list(
        self,
        session_id: UUID
    ) -> list[AdminUserAttendanceRead]:
        ...

    async def is_session_attended(
        self,
        session_id: UUID
    ) -> bool:
        ...
