from app.infrastructure.persistence.in_memory.storage import (
    InMemoryAuthStorage
)
from app.infrastructure.persistence.in_memory.repositories.auth import (
    InMemoryAuthCreationRepository,
    InMemoryAuthReadRepository,
    InMemoryAuthUpdateRepository
)
from app.feature.auth.uow.login_uow import (
    LoginUoWPort
)


class InMemoryLoginUoW(LoginUoWPort):
    def __init__(self, storage: InMemoryAuthStorage) -> None:
        self.auth_read = InMemoryAuthReadRepository(storage)
        self.auth_update = InMemoryAuthUpdateRepository(storage)
        self.auth_creation = InMemoryAuthCreationRepository(storage)
