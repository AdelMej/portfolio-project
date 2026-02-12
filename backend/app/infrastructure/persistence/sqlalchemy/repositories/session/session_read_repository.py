from datetime import datetime
from uuid import UUID
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.sql.expression import text
from app.domain.session.session_entity import SessionEntity
from app.domain.session.session_status import SessionStatus
from app.feature.session.repositories.session_read_repository_port import (
    SessionReadRepositoryPort
)


class SqlAlchemySessionReadRepository(SessionReadRepositoryPort):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_session_by_id(
        self,
        session_id: UUID
    ) -> SessionEntity | None:
        result = await self._session.execute(
            text(
                """SELECT
                    id,
                    coach_id,
                    title,
                    starts_at,
                    ends_at,
                    status::text,
                    cancelled_at,
                    price_cents,
                    currency
                FROM app.sessions
                WHERE id=:id
                """
            ),
            {
                'id': session_id
            }
        )

        row = result.mappings().one_or_none()
        if not row:
            return None

        return SessionEntity(
            id=row["id"],
            coach_id=row["coach_id"],
            title=row["title"],
            starts_at=row["starts_at"],
            ends_at=row["ends_at"],
            status=SessionStatus(row["status"]),
            cancelled_at=row["cancelled_at"],
            price_cents=row["price_cents"],
            currency=row["currency"]
        )

    async def get_all_sessions(
        self,
        offset: int,
        limit: int,
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
                currency=row["currency"]
            ) for row in rows
        ], has_more

    async def get_sessions_by_coach_id(
        self,
        coach_id: UUID,
        offset: int,
        limit: int,
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
                currency=row["currency"]
            ) for row in rows
        ], has_more

    async def get_attendance(self, session_id: UUID) -> list[UUID]:
        result = await self._session.execute(
            text(
                """
                SELECT user_id
                FROM app.session_attendance
                WHERE session_id = :session_id
                """
            ),
            {"session_id": session_id},
        )

        return [row.user_id for row in result.fetchall()]
