from datetime import datetime
from pydantic import BaseModel
from uuid import UUID


class GetPaymentOutputDTO(BaseModel):
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


class PaginatedPaymentOutputDTO(BaseModel):
    items: list[GetPaymentOutputDTO]
    limit: int
    offset: int
    has_more: bool


class GetCoachPaymentOutputDTO(BaseModel):
    id: UUID
    session_id: UUID
    coach_id: UUID
    provider: str
    provider_payment_id: str
    gross_amount_cents: int
    provider_fee_cents: int
    net_amount_cents: int
    currency: str
    created_at: datetime


class PaginatedCoachPaymentOutputDTO(BaseModel):
    items: list[GetCoachPaymentOutputDTO]
    limit: int
    offset: int
    has_more: bool
