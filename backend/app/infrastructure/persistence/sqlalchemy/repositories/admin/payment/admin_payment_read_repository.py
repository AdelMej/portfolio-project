from datetime import datetime
from uuid import UUID

from sqlalchemy import text
from sqlalchemy.ext.asyncio.session import AsyncSession
from app.domain.payment.payment_entity import PaymentEntity
from app.feature.admin.payment.repositories import (
    AdminPaymentReadRepoPort
)


class SqlAlchemyAdminPaymentReadRepo(AdminPaymentReadRepoPort):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_all_payments(
        self,
        offset: int,
        limit: int,
        _from: datetime | None,
        to: datetime | None,
    ) -> tuple[list[PaymentEntity], bool]:
        stmt = text("""
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
            WHERE (
                CAST(:from_ts AS TIMESTAMPTZ) IS NULL
                OR created_at >= CAST(:from_ts AS TIMESTAMPTZ)
                )
            AND (
                CAST(:to_ts AS TIMESTAMPTZ) IS NULL
                OR CAST(:to_ts AS TIMESTAMPTZ) <= created_at
            )
            LIMIT :limit
            OFFSET :offset
        """)

        rows = await self._session.execute(stmt, {
            "from_ts": _from,
            "to_ts": to,
            "limit": limit + 1,
            "offset": offset
        })

        rows = rows.mappings().all()
        has_more = len(rows) > limit

        rows = rows[:limit]

        return [
            PaymentEntity(
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

    async def get_user_payments(
        self,
        offset: int,
        limit: int,
        _from: datetime | None,
        to: datetime | None,
        user_id: UUID
    ) -> tuple[list[PaymentEntity], bool]:
        stmt = text("""
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
            WHERE user_id = :user_id
            AND (
                CAST(:from_ts AS TIMESTAMPTZ) IS NULL
                OR created_at >= CAST(:from_ts AS TIMESTAMPTZ)
                )
            AND (
                CAST(:to_ts AS TIMESTAMPTZ) IS NULL
                OR CAST(:to_ts AS TIMESTAMPTZ) <= created_at
            )
            LIMIT :limit
            OFFSET :offset
        """)

        rows = await self._session.execute(stmt, {
            "user_id": user_id,
            "from_ts": _from,
            "to_ts": to,
            "limit": limit + 1,
            "offset": offset
        })

        rows = rows.mappings().all()
        has_more = len(rows) > limit

        rows = rows[:limit]

        return [
            PaymentEntity(
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

    async def get_coach_payments(
        self,
        offset: int,
        limit: int,
        _from: datetime | None,
        to: datetime | None,
        coach_id: UUID
    ) -> tuple[list[PaymentEntity], bool]:
        stmt = text("""
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
            WHERE user_id = :coach_id
            AND (
                CAST(:from_ts AS TIMESTAMPTZ) IS NULL
                OR created_at >= CAST(:from_ts AS TIMESTAMPTZ)
                )
            AND (
                CAST(:to_ts AS TIMESTAMPTZ) IS NULL
                OR CAST(:to_ts AS TIMESTAMPTZ) <= created_at
            )
            LIMIT :limit
            OFFSET :offset
        """)

        rows = await self._session.execute(stmt, {
            "coach_id": coach_id,
            "from_ts": _from,
            "to_ts": to,
            "limit": limit + 1,
            "offset": offset
        })

        rows = rows.mappings().all()
        has_more = len(rows) > limit

        rows = rows[:limit]

        return [
            PaymentEntity(
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
