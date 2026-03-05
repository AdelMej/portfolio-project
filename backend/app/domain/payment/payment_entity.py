from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass(frozen=True)
class PaymentEntity:
    id: UUID
    session_id: UUID
    user_id: UUID
    provider: str
    provider_payment_id: str
    gross_amount_cents: int
    provider_fee_cents: int
    net_amount_cents: int
    currency: str
    created_at: datetime


@dataclass(frozen=True)
class NewPaymentEntity:
    session_id: UUID
    user_id: UUID
    provider: str
    provider_payment_id: str
    gross_amount_cents: int
    provider_fee_cents: int
    net_amount_cents: int
    currency: str
