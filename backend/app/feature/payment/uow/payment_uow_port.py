from typing import Protocol
from app.feature.payment.repostories.payment_read_repository import (
    PaymentReadRepositoryPort
)


class PaymentUoWPort(Protocol):
    payment_read_repository: PaymentReadRepositoryPort
