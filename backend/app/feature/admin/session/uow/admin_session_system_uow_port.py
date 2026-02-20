from typing import Protocol

from app.feature.admin.session.repositories import (
    AuthReadRepoPort,
    AdminSessionReadRepoPort,
    AdminSessionUpdateRepoPort
)


class AdminSessionSystemUoWPort(Protocol):
    auth_read_repo: AuthReadRepoPort
    session_read_repo: AdminSessionReadRepoPort
    session_update_repo: AdminSessionUpdateRepoPort
