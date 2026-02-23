from typing import Protocol

from app.feature.credit.respositories import (
    CreditLedgerReadRepoPort,
    AuthReadRepoPort
)


class CreditUoWPort(Protocol):
    credit_read_repo: CreditLedgerReadRepoPort
    auth_read_repo: AuthReadRepoPort
