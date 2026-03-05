from typing import Protocol
from app.feature.payment.repostories import (
    PaymentReadRepoPort,
    AuthReadRepoPort
)


class PaymentUoWPort(Protocol):
    payment_read_repo: PaymentReadRepoPort
    auth_read_repo: AuthReadRepoPort
