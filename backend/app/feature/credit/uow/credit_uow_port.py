from typing import Protocol

from app.feature.credit.respositories import (
    CreditLedgerReadRepoPort
)


class CreditUoWPort(Protocol):
    credit_read_repo: CreditLedgerReadRepoPort
