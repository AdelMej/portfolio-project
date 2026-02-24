from typing import Protocol
from uuid import UUID


class PaymentReadRepoPort(Protocol):
    async def is_alread_paid(
        self,
        session_id: UUID,
        user_id: UUID
    ) -> bool:
        ...

    async def get_payment_for_session(
        self,
        session_id: UUID
    ) -> tuple[int, str]:
        ...
