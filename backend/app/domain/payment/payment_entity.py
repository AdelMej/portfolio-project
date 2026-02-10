from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass(frozen=True)
class PaymentEnity:
    id: UUID
    session_id: UUID
    user_id: UUID
    provider: str
    provider_payment_id: str
    amount_cents: int
    currency: str
    created_at: datetime
