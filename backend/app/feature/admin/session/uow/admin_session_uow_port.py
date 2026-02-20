from typing import Protocol

from app.feature.admin.session.repositories import (
    AdminSessionReadRepoPort,
    AdminSessionUpdateRepoPort,
    AuthReadRepoPort,
    AdminSessionAttendanceReadRepoPort
)


class AdminSessionUoWPort(Protocol):
    session_read_repo: AdminSessionReadRepoPort
    session_update_repo: AdminSessionUpdateRepoPort
    auth_read_repo: AuthReadRepoPort
    session_attendance_read_repo: AdminSessionAttendanceReadRepoPort
