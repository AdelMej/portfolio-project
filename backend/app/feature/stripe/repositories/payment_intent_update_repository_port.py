from typing import Protocol
from uuid import UUID

from app.domain.payment_intent.payment_intent_providers import PaymentProvider


class PaymentIntentUpdateRepoPort(Protocol):
    async def mark_payment_intent(
        self,
        provider_payment_id: str,
        provider_status: str,
    ) -> None:
        ...

    async def set_provider_id(
        self,
        user_id: UUID,
        session_id: UUID,
        provider: PaymentProvider,
        provider_intent_id: str
    ) -> None:
        ...
