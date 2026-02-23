from typing import Protocol
from uuid import UUID


class MeUpdateRepoPort(Protocol):
    async def update_email_by_user_id(self, email: str, user_id: UUID):
        ...

    async def update_password_by_id(self, user_id: UUID, password_hash: str):
        ...

    async def update_profile_by_id(
        self,
        user_id: UUID,
        first_name: str,
        last_name: str
    ):
        ...
