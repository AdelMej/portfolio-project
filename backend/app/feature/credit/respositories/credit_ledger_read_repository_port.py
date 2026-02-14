from datetime import datetime
from typing import Protocol
from uuid import UUID

from app.domain.credit.credit_entity import CreditEntity


class CreditLedgerReadRepoPort(Protocol):
    async def get_credit_by_user_id(
        self,
        limit: int,
        offset: int,
        _from: datetime | None,
        to: datetime | None,
        user_id: UUID
    ) -> tuple[list[CreditEntity], bool]:
        ...
