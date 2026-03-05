from typing import Protocol
from app.domain.credit.credit_entity import NewCreditEntity


class CreditLedgerCreationRepoPort(Protocol):
    async def append_credit_ledger(
        self,
        credit: NewCreditEntity
    ) -> None:
        ...
