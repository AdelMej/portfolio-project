from typing import Protocol
from uuid import UUID


class CreditLedgerReadRepoPort(Protocol):
    async def fetch_credit_by_user_id(
        self,
        user_id: UUID,
        currency: str
    ) -> int:
        ...
