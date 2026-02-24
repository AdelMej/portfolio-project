from datetime import datetime
from typing import Protocol
from uuid import UUID

from app.domain.payment.payment_entity import PaymentEntity


class AdminPaymentReadRepoPort(Protocol):
    async def get_all_payments(
        self,
        offset: int,
        limit: int,
        _from: datetime | None,
        to: datetime | None,
    ) -> tuple[list[PaymentEntity], bool]:
        ...

    async def get_user_payments(
        self,
        offset: int,
        limit: int,
        _from: datetime | None,
        to: datetime | None,
        user_id: UUID
    ) -> tuple[list[PaymentEntity], bool]:
        ...

    async def get_coach_payments(
        self,
        offset: int,
        limit: int,
        _from: datetime | None,
        to: datetime | None,
        coach_id: UUID
    ) -> tuple[list[PaymentEntity], bool]:
        ...
