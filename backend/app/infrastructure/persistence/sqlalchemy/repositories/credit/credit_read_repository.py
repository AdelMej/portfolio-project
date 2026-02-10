from datetime import datetime
from uuid import UUID
from sqlalchemy import text
from sqlalchemy.ext.asyncio.session import AsyncSession
from app.domain.credit.credit_entity import CreditEntity
from app.feature.credit.respositories.credit_read_repository_port import (
    CreditReadRepositoryPort
)


class SqlAlchemyCreditReadRepository(CreditReadRepositoryPort):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_credit_by_user_id(
        self,
        limit: int,
        offset: int,
        _from: datetime | None,
        to: datetime | None,
        user_id: UUID
    ) -> tuple[list[CreditEntity], bool]:
        res = await self._session.execute(
            text(
                """
                SELECT
                    amount_cents,
                    balance_after_cents,
                    cause,
                    created_at
                FROM app.credit_ledger
                WHERE
                    user_id = :user_id
                    AND (
                        CAST(:from_ts as timestamptz) IS NULL
                        OR created_at >= CAST(:from_ts as timestamptz)
                    )
                    AND (
                        CAST(:to as timestamptz) IS NULL
                        OR created_at <= CAST(:to as timestamptz)
                    )
                ORDER BY created_at DESC
                LIMIT :limit
                OFFSET :offset
                """
            ),
            {
                "user_id": user_id,
                "from_ts": _from,
                "to": to,
                "offset": offset,
                "limit": limit + 1
            }
        )

        rows = res.mappings().all()

        has_more = len(rows) > limit
        rows = rows[:limit]

        return [
            CreditEntity(
                amount_cents=row["amount_cents"],
                balance_after_cents=row["balance_after_cents"],
                cause=row["cause"],
                created_at=row["created_at"]
            ) for row in rows
        ], has_more
