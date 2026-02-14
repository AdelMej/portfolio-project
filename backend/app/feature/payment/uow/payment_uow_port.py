from typing import Protocol
from app.feature.payment.repostories.payment_read_repository import (
    PaymentReadRepoPort
)


class PaymentUoWPort(Protocol):
    payment_read_repo: PaymentReadRepoPort
