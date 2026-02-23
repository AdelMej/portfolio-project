from datetime import datetime
from uuid import UUID
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.sql import text
from app.domain.session.session_entity import SessionEntity
from app.domain.session.session_status import SessionStatus
from app.feature.admin.session.repositories import (
    AdminSessionReadRepoPort
)


class SqlAlchemyAdminSessionReadRepo(AdminSessionReadRepoPort):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def sessions_by_coach_id(
        self,
        coach_id: UUID,
        limit: int,
        offset: int,
        _from: datetime | None,
        to: datetime | None
    ) -> tuple[list[SessionEntity], bool]:
        res = await self._session.execute(
            text("""
                SELECT
                    id,
                    coach_id,
                    title,
                    starts_at,
                    ends_at,
                    status::text,
                    cancelled_at,
                    price_cents,
                    currency,
                    created_at,
                    updated_at
                FROM app.sessions
                WHERE coach_id = :coach_id
                AND (
                    CAST(:from_ts as timestamptz) IS NULL
                    OR starts_at >= CAST(:from_ts as timestamptz)
                )
                AND (
                    CAST(:to_ts as timestamptz) IS NULL
                    OR ends_at <= CAST(:to_ts as timestamptz)
                )
                ORDER BY created_at DESC
                LIMIT :limit
                OFFSET :offset
            """),
            {
                "coach_id": coach_id,
                "from_ts": _from,
                "to_ts": to,
                "limit": limit + 1,
                "offset": offset
            }
        )

        rows = res.mappings().all()
        has_more = len(rows) > limit
        rows[:limit]

        return [
            SessionEntity(
                id=row["id"],
                coach_id=row["coach_id"],
                title=row["title"],
                starts_at=row["starts_at"],
                ends_at=row["ends_at"],
                status=SessionStatus(row["status"]),
                cancelled_at=row["cancelled_at"],
                price_cents=row["price_cents"],
                currency=row["currency"],
                created_at=row["created_at"],
                updated_at=row["updated_at"]
            ) for row in rows
        ], has_more

    async def get_all_sessions(
        self,
        limit: int,
        offset: int,
        _from: datetime | None,
        to: datetime | None
    ) -> tuple[list[SessionEntity], bool]:
        res = await self._session.execute(
            text("""
                SELECT
                    id,
                    coach_id,
                    title,
                    starts_at,
                    ends_at,
                    status::text,
                    cancelled_at,
                    price_cents,
                    currency,
                    created_at,
                    updated_at
                FROM app.sessions
                WHERE (
                    CAST(:from_ts as timestamptz) IS NULL
                    OR starts_at >= CAST(:from_ts as timestamptz)
                )
                AND (
                    CAST(:to_ts as timestamptz) IS NULL
                    OR ends_at <= CAST(:to_ts as timestamptz)
                )
                AND cancelled_at IS NULL
                ORDER BY created_at DESC
                LIMIT :limit
                OFFSET :offset
            """),
            {
                "from_ts": _from,
                "to_ts": to,
                "limit": limit + 1,
                "offset": offset
            }
        )

        rows = res.mappings().all()
        has_more = len(rows) > limit
        rows[:limit]

        return [
            SessionEntity(
                id=row["id"],
                coach_id=row["coach_id"],
                title=row["title"],
                starts_at=row["starts_at"],
                ends_at=row["ends_at"],
                status=SessionStatus(row["status"]),
                cancelled_at=row["cancelled_at"],
                price_cents=row["price_cents"],
                currency=row["currency"],
                created_at=row["created_at"],
                updated_at=row["updated_at"]
            ) for row in rows
        ], has_more

    async def exist_session(
        self,
        session_id: UUID
    ) -> bool:
        result = await self._session.execute(
            text("""
                SELECT
                    app_fcn.session_exists(:session_id)
            """),
            {
                "session_id": session_id
            }
        )
        return result.scalar_one()

    async def is_session_owner(
        self,
        session_id: UUID,
        user_id: UUID
    ) -> bool:
        result = await self._session.execute(
            text("""
                SELECT
                    app_fcn.is_session_owner(
                        :user_id,
                        :session_id
                    )
            """),
            {
                "user_id": user_id,
                "session_id": session_id
            }
        )

        return result.scalar_one()

    async def is_session_cancelled(
        self,
        session_id: UUID
    ) -> bool:
        result = await self._session.execute(
            text("""
                SELECT
                    app_fcn.is_session_cancelled(:session_id)
            """),
            {
                "session_id": session_id
            }
        )

        return result.scalar_one()

    async def is_session_started(
        self,
        session_id: UUID
    ) -> bool:
        stmt = text("""
            SELECT
                app_fcn.is_session_started(
                    :session_id
                )
        """)

        res = await self._session.execute(stmt, {
            "session_id": session_id
        })

        return res.scalar_one()
