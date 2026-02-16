from typing import Protocol

from app.feature.session.repositories.session_read_repository_port import (
    SessionReadRepoPort
)


class SessionPulbicUoWPort(Protocol):
    session_read_repo: SessionReadRepoPort
