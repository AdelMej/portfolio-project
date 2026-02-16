from datetime import datetime
from uuid import UUID
from sqlalchemy import text
from sqlalchemy.exc import DBAPIError
from sqlalchemy.ext.asyncio.session import AsyncSession
from app.domain.auth.auth_exceptions import PermissionDeniedError
from app.domain.credit.credit_entity import CreditEntity
from app.feature.credit.respositories import (
    CreditLedgerReadRepoPort
)
from app.shared.database.sqlstate_extractor import get_sqlstate


class SqlAlchemyCreditLedgerReadRepo(CreditLedgerReadRepoPort):
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
                    id,
                    user_id,
                    payment_id,
                    amount_cents,
                    currency,
                    balance_after_cents,
                    cause,
                    created_at
                FROM app.credit_ledger
                WHERE
                    user_id = :user_id
                    AND (
                        CAST(:from_ts as timestamptz) IS NULL
                        OR created_at >= CAST(:from_ts AS timestamptz)
                    )
                    AND (
                        CAST(:to_ts as timestamptz) IS NULL
                        OR created_at <= CAST(:to_ts AS timestamptz)
                    )
                ORDER BY created_at DESC
                LIMIT :limit
                OFFSET :offset
                """
            ),
            {
                "user_id": user_id,
                "from_ts": _from,
                "to_ts": to,
                "offset": offset,
                "limit": limit + 1
            }
        )

        rows = res.mappings().all()

        has_more = len(rows) > limit
        rows = rows[:limit]

        return [
            CreditEntity(
                id=row["id"],
                user_id=row['user_id'],
                payment_id=row['payment_id'],
                amount_cents=row["amount_cents"],
                currency=row["currency"],
                balance_after_cents=row["balance_after_cents"],
                cause=row["cause"],
                created_at=row["created_at"]
            ) for row in rows
        ], has_more

    async def fetch_credit_by_user_id(
        self,
        user_id: UUID,
        currency: str
    ) -> int:
        stmt = text("""
            SELECT
                app_fcn.fetch_credit(
                    :user_id,
                    :currency
                )
        """)

        try:
            result = await self._session.execute(stmt, {
                "user_id": user_id,
                "currency": currency
            })
        except DBAPIError as exc:
            code = get_sqlstate(exc)

            if code == 'AP401':
                raise PermissionDeniedError() from exc

            raise

        return result.scalar_one()
