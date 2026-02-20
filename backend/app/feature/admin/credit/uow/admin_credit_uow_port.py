from typing import Protocol

from app.feature.admin.credit.repositories import (
    AdminCreditLedgerReadRepoPort
)


class AdminCreditUoWPort(Protocol):
    credit_read_repo: AdminCreditLedgerReadRepoPort
