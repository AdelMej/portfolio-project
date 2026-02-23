from typing import Protocol

from app.feature.admin.credit.repositories import (
    AdminCreditLedgerReadRepoPort,
    AuthReadRepoPort
)


class AdminCreditUoWPort(Protocol):
    credit_read_repo: AdminCreditLedgerReadRepoPort
    auth_read_repo: AuthReadRepoPort
