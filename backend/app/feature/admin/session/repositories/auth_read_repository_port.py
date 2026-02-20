from typing import Protocol


class AuthReadRepoPort(Protocol):
    async def is_user_disabled(
        self,
        user_id
    ) -> bool:
        ...
