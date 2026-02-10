from typing import Protocol
from app.feature.credit.respositories.credit_read_repository_port import (
    CreditReadRepositoryPort
)


class CreditUoWPort(Protocol):
    credit_read_repository: CreditReadRepositoryPort
