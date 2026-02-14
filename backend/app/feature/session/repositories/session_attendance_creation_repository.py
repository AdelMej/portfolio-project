from typing import Protocol
from uuid import UUID


class SessionAttendanceCreationRepoPort(Protocol):
    async def create_attendance(
        self,
        session_id: UUID,
        attendance_list: dict[UUID, bool]
    ) -> None:
        ...
