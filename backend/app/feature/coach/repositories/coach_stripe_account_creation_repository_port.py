from typing import Protocol


class CoachStripeAccountCreationRepoPort(Protocol):
    async def create_account(
        self,
        stripe_acount_id: str
    ) -> None:
        ...
