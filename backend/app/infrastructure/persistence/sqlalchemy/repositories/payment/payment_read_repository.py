from datetime import datetime
from uuid import UUID
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.sql import text
from app.domain.payment.payment_entity import PaymentEnity
from app.feature.payment.repostories.payment_read_repository import (
    PaymentReadRepoPort
)


class SqlAlchemyPaymentReadRepo(PaymentReadRepoPort):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_payment_by_user_id(
        self,
        offset: int,
        limit: int,
        _from: datetime | None,
        to: datetime | None,
        user_id: UUID
    ) -> tuple[list[PaymentEnity], bool]:
        res = await self._session.execute(
            text("""
                SELECT
                    id,
                    session_id,
                    user_id,
                    provider,
                    provider_payment_id,
                    gross_amount_cents,
                    provider_fee_cents,
                    net_amount_cents,
                    currency,
                    created_at
                FROM app.payments
                WHERE
                    user_id = :user_id
                    AND (
                        CAST(:from_ts AS timestamptz) IS NULL
                        OR created_at >= CAST(:from_ts AS timestamptz)
                    )
                    AND (
                        CAST(:to_ts AS timestamptz) IS NULL
                        OR created_at <= CAST(:to_ts AS timestamptz)
                    )
                ORDER BY created_at DESC
                LIMIT :limit
                OFFSET :offset
            """),
            {
                "user_id": user_id,
                "from_ts": _from,
                "to_ts": to,
                "limit": limit + 1,
                "offset": offset
            }
        )

        rows = res.mappings().all()

        has_more = len(rows) > limit
        rows = rows[:limit]

        return [
            PaymentEnity(
                id=row["id"],
                session_id=row["session_id"],
                user_id=row["user_id"],
                provider=row["provider"],
                provider_payment_id=row["provider_payment_id"],
                gross_amount_cents=row["gross_amount_cents"],
                provider_fee_cents=row["provider_fee_cents"],
                net_amount_cents=row["net_amount_cents"],
                currency=row["currency"],
                created_at=row["created_at"]
            ) for row in rows
        ], has_more

    async def is_alread_paid(
        self,
        session_id: UUID,
        user_id: UUID
    ) -> bool:
        stmt = text("""
            SELECT
                app_fcn.is_already_paid(
                    :session_id,
                    :user_id
                )
        """)

        res = await self._session.execute(stmt, {
            "session_id": session_id,
            "user_id": user_id
        })

        return res.scalar_one()

    async def get_payment_for_session(
        self,
        session_id: UUID
    ) -> tuple[int, str]:
        stmt = text("""
            SELECT *
            FROM app_fcn.get_payment_for_session(
                    :session_id
                )
        """)

        res = await self._session.execute(stmt, {
            "session_id": session_id
        })

        row = res.mappings().one()

        return row["amount_cents"], row["currency"]
