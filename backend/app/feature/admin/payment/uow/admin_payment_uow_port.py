from typing import Protocol

from app.feature.admin.payment.repositories import (
    AdminPaymentReadRepoPort
)
from app.feature.admin.payment.repositories import (
    AuthReadRepoPort
)


class AdminPaymentUoWPort(Protocol):
    payment_read_repo: AdminPaymentReadRepoPort
    auth_read_repo: AuthReadRepoPort
