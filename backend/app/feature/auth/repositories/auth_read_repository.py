from typing import Protocol
from app.domain.user.user_entity import User


class AuthReadRepositoryPort(Protocol):
    async def exist_email(self, email: str) -> bool:
        ...

    async def get_user_by_email(self, email: str) -> User:
        ...
