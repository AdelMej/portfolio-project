from app.feature.auth.auth_UoW_port import AuthUoW
from .auth_read_repo import InMemoryAuthReadRepo
from .auth_update_repo import InMemoryAuthUpdateRepo
from .auth_creation_repository import InMemoryAuthCreationRepository
from ..storage import InMemoryAuthStorage


class InMemoryAuthUoW(AuthUoW):
    def __init__(self, storage: InMemoryAuthStorage) -> None:
        self._storage = storage

    async def __aenter__(self):
        self.auth_read = InMemoryAuthReadRepo(self._storage)
        self.auth_update = InMemoryAuthUpdateRepo(self._storage)
        self.auth_creation = InMemoryAuthCreationRepository(self._storage)
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        return None
