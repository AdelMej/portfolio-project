from typing import Protocol
from uuid import UUID


class CoachStripeAccountReadRepoPort(Protocol):
    async def is_coach_account_valid(
        self,
        coach_id: UUID
    ) -> bool:
        ...
