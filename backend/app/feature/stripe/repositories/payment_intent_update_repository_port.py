from typing import Protocol


class PaymentIntentUpdateRepoPort(Protocol):
    async def mark_payment_intent(
        self,
        provider_payment_id: str,
        provider_status: str
    ) -> None:
        ...
