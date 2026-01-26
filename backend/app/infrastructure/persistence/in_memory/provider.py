from fastapi import Depends
from app.infrastructure.persistence.in_memory.storage import (
    InMemoryAuthStorage
)
from app.feature.auth.uow.login_uow import LoginUoWPort
from app.infrastructure.persistence.in_memory.uow.auth import InMemoryLoginUoW
from functools import lru_cache


@lru_cache
def get_in_memory_storage() -> InMemoryAuthStorage:
    return InMemoryAuthStorage()


def get_in_memory_login_uow(
        storage: InMemoryAuthStorage = Depends(get_in_memory_storage)
) -> LoginUoWPort:
    return InMemoryLoginUoW(storage)
