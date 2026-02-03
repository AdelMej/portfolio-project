from app.infrastructure.persistence.in_memory.storage import (
    InMemoryAuthStorage
)
from app.feature.auth.repositories.auth_creation_respository_port import (
    AuthCreationRepositoryPort
)


class InMemoryAuthCreationRepository(AuthCreationRepositoryPort):
    def __init__(self, storage: InMemoryAuthStorage) -> None:
        self._storage = storage
