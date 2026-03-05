from typing import Protocol

from app.domain.payment.payment_entity import NewPaymentEntity


class PaymentCreationRepoPort(Protocol):
    async def create_payment(
        self,
        new_payment: NewPaymentEntity
    ) -> None:
        ...
