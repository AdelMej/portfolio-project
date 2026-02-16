from datetime import datetime
from typing import Protocol
from uuid import UUID

from app.domain.payment.payment_entity import PaymentEnity


class PaymentReadRepoPort(Protocol):
    async def get_payment_by_user_id(
        self,
        offset: int,
        limit: int,
        _from: datetime | None,
        to: datetime | None,
        user_id: UUID
    ) -> tuple[list[PaymentEnity], bool]:
        ...
