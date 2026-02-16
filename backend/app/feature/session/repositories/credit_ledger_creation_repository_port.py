from typing import Protocol

from app.domain.credit.credit_entity import NewCreditEntity


class CreditLedgerCreationRepoPort(Protocol):
    async def create_credit_entry(
        self,
        entry: NewCreditEntity
    ) -> None:
        ...
