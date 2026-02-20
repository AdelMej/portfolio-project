from typing import Protocol

from app.feature.admin.payment.repositories import (
    AdminPaymentReadRepoPort
)


class AdminPaymentUoWPort(Protocol):
    payment_read_repo: AdminPaymentReadRepoPort
