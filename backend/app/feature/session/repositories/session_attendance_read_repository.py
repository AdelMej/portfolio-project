from typing import Protocol
from uuid import UUID

from app.domain.user.user_profile_entity import UserProfileEntity


class SessionAttendanceReadRepoPort(Protocol):
    async def is_session_attended(
        self,
        session_id: UUID
    ) -> bool:
        ...

    async def get_attendance(
        self,
        session_id: UUID
    ) -> list[UserProfileEntity]:
        ...

    async def is_session_attendance_open(
        self,
        session_id: UUID
    ) -> bool:
        ...

    async def is_attendance_payload_valid(
        self,
        session_id: UUID,
        attendance_list: dict[UUID, bool]
    ) -> bool:
        ...
