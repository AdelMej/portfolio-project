from typing import Protocol
from uuid import UUID


class CoachStripeAccountReadRepoPort(Protocol):
    async def get_account_id(
        self,
        coach_id: UUID
    ) -> str | None:
        ...
