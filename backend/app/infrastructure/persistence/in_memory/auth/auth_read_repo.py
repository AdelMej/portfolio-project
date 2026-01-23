from app.infrastructure.persistence.in_memory.storage import (
    InMemoryAuthStorage
)


class InMemoryAuthReadRepo:
    def __init__(self, storage: InMemoryAuthStorage) -> None:
        self._storage = storage

    async def exist_email(self, email: str) -> bool:
        return email in self._storage.users_by_email

    async def get_user_by_email(self, email: str):
        user_id = self._storage.users_by_email[email]
        return self._storage.users[user_id]
