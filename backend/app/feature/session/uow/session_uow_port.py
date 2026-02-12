from typing import Protocol
from app.feature.session.repositories.session_creation_repository_port import (
    SessionCreationRepositoryPort
)
from app.feature.session.repositories.session_read_repository_port import (
    SessionReadRepositoryPort
)
from app.feature.session.repositories.session_update_repository_port import (
    SessionUpdateRepositoryPort
)
from app.feature.auth.repositories.auth_read_repository_port import (
    AuthReadRepositoryPort
)


class SessionUoWPort(Protocol):
    session_creation_repository: SessionCreationRepositoryPort
    session_update_repository: SessionUpdateRepositoryPort
    session_read_repository: SessionReadRepositoryPort
    auth_read_repository: AuthReadRepositoryPort
