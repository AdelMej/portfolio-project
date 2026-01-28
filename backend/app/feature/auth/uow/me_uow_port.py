from typing import Protocol
from app.feature.auth.repositories.me_read_repository_port import (
    MeReadRepositoryPort
)


class MeUoWPort(Protocol):
    me_read_repository: MeReadRepositoryPort
