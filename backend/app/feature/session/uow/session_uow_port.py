from typing import Protocol
from app.feature.session.repositories.session_creation_repository_port import (
    SessionCreationRepositoryPort
)
from app.feature.session.repositories.session_update_repository_port import (
    SessionUpdateRepositoryPort
)


class SessionUoWPort(Protocol):
    session_creation_repository: SessionCreationRepositoryPort
    session_update_repository: SessionUpdateRepositoryPort
