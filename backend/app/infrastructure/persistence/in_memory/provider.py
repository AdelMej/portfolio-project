from fastapi import Depends
from app.infrastructure.persistence.in_memory.auth.auth_uow import (
    InMemoryAuthUoW
)
from app.infrastructure.persistence.in_memory.storage import (
    InMemoryAuthStorage
)
from app.feature.auth.auth_UoW_port import AuthUoW


def get_in_memory_storage() -> InMemoryAuthStorage:
    return InMemoryAuthStorage()


def get_in_memory_auth_uow(
        storage: InMemoryAuthStorage = Depends(get_in_memory_storage)
) -> AuthUoW:
    return InMemoryAuthUoW(storage)
