from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass(frozen=True)
class PaymentParticipationEntity():
    id: UUID
    session_id: UUID
    user_id: UUID
    paid_at: datetime
    registred_at: datetime
    cancelled_at: datetime


@dataclass(frozen=True)
class NewPaymentParticipationEntity():
    session_id: UUID
    user_id: UUID
