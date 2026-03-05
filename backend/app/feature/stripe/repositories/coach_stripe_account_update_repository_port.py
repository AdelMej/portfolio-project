from typing import Protocol


class CoachStripeAccountUpdateRepoPort(Protocol):
    async def update_by_account_id(
        self,
        account_id: str,
        details_submitted: bool,
        charges_enabled: bool,
        payouts_enabled: bool
    ) -> None:
        ...
