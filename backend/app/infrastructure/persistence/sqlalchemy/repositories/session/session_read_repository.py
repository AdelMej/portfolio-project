from datetime import datetime
from uuid import UUID
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.sql.expression import text
from app.domain.session.session_entity import (
    SessionCompleteEntity,
    SessionEntity,
    SessionWithCoachEntity
)
from app.domain.session.session_status import SessionStatus
from app.domain.user.user_profile_entity import UserProfileEntity
from app.feature.session.repositories.session_read_repository_port import (
    SessionReadRepoPort
)


class SqlAlchemySessionReadRepo(SessionReadRepoPort):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_session_by_id(
        self,
        session_id: UUID
    ) -> SessionWithCoachEntity:
        result = await self._session.execute(
            text(
                """SELECT
                    s.id,
                    cp.user_id as coach_id,
                    cp.first_name,
                    cp.last_name,
                    s.title,
                    s.starts_at,
                    s.ends_at,
                    s.status::text,
                    s.cancelled_at,
                    s.price_cents,
                    s.currency,
                    s.created_at,
                    s.updated_at
                FROM app.sessions s
                JOIN app.v_coach_public cp ON cp.user_id = s.coach_id
                WHERE id=:id
                """
            ),
            {
                'id': session_id
            }
        )

        row = result.mappings().one()

        return SessionWithCoachEntity(
            id=row["id"],
            coach=UserProfileEntity(
                user_id=row["coach_id"],
                first_name=row["first_name"],
                last_name=row["last_name"]
            ),
            title=row["title"],
            starts_at=row["starts_at"],
            ends_at=row["ends_at"],
            status=SessionStatus(row["status"]),
            cancelled_at=row["cancelled_at"],
            price_cents=row["price_cents"],
            currency=row["currency"],
            created_at=row["created_at"],
            updated_at=row["updated_at"]
        )

    async def get_all_sessions(
        self,
        offset: int,
        limit: int,
        _from: datetime | None,
        to: datetime | None
    ) -> tuple[list[SessionWithCoachEntity], bool]:
        res = await self._session.execute(
            text("""
                SELECT
                    s.id,
                    cp.user_id as coach_id,
                    cp.first_name,
                    cp.last_name,
                    s.title,
                    s.starts_at,
                    s.ends_at,
                    s.status::text,
                    s.cancelled_at,
                    s.price_cents,
                    s.currency,
                    s.created_at,
                    s.updated_at
                FROM app.sessions s
                JOIN app.v_coach_public cp ON cp.user_id = s.coach_id
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
            SessionWithCoachEntity(
                id=row["id"],
                coach=UserProfileEntity(
                    user_id=row["coach_id"],
                    first_name=row["first_name"],
                    last_name=row["last_name"]
                ),
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
                currency=row["currency"],
                created_at=row["created_at"],
                updated_at=row["updated_at"]
            ) for row in rows
        ], has_more

    async def is_session_overlapping(
        self,
        starts_at: datetime,
        ends_at: datetime
    ) -> bool:
        res = await self._session.execute(
            text("""
                    SELECT
                        app_fcn.is_session_overlapping(:starts_at, :ends_at)
            """),
            {
                "starts_at": starts_at,
                "ends_at": ends_at
            }
        )

        return res.scalar_one()

    async def is_session_overlapping_except(
        self,
        starts_at: datetime,
        ends_at: datetime,
        except_session_id: UUID
    ) -> bool:
        result = await self._session.execute(
            text("""
                SELECT
                    app_fcn.is_session_overlapping_except(
                        :starts_at,
                        :ends_at,
                        :except_session
                    )
            """),
            {
                "starts_at": starts_at,
                "ends_at": ends_at,
                "except_session": except_session_id
            }
        )

        return result.scalar_one()

    async def public_exists_session(
        self,
        session_id: UUID
    ) -> bool:
        stmt = text("""
            SELECT EXISTS(
                SELECT 1
                FROM app.sessions
                WHERE id = :session_id
            )
        """)

        res = await self._session.execute(stmt,  {
            "session_id": session_id
        })

        return res.scalar_one()

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

    async def system_get_session_by_id(
        self,
        session_id: UUID
    ) -> SessionEntity:
        stmt = text("""
            SELECT *
            FROM app_fcn.get_session_for_registration(
                :session_id
            )
        """)

        result = await self._session.execute(stmt, {
            "session_id": session_id
        })

        row = result.mappings().one()

        return SessionEntity(
            id=row["id"],
            coach_id=row["coach_id"],
            title=row["title"],
            starts_at=row["starts_at"],
            ends_at=row["ends_at"],
            status=row["status"],
            cancelled_at=row["cancelled_at"],
            price_cents=row["price_cents"],
            currency=row["currency"],
            created_at=row["created_at"],
            updated_at=row["updated_at"]
        )

    async def is_session_finished(
        self,
        session_id: UUID
    ) -> bool:
        stmt = text("""
            SELECT
                app_fcn.is_session_finished(
                    :session_id
                )
        """)

        res = await self._session.execute(stmt, {
            "session_id": session_id
        })

        return res.scalar_one()

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

    async def get_own_sessions(
        self,
        user_id: UUID,
        limit: int,
        offset: int,
        _from: datetime | None,
        to: datetime | None
    ) -> tuple[list[SessionCompleteEntity], bool]:
        stmt = text("""
        SELECT
            s.id,
            cp.user_id,
            cp.first_name,
            cp.last_name,
            s.title,
            s.starts_at,
            s.ends_at,
            s.status,
            s.cancelled_at,
            s.price_cents,
            s.currency,
            s.created_at,
            s.updated_at,
            COALESCE(
                array_agg(
                    json_build_object(
                        'user_id', up.user_id,
                        'first_name', up.first_name,
                        'last_name', up.last_name
                    )
                ) FILTER (WHERE up.user_id IS NOT NULL),
                '{}'
            ) AS participants
        FROM app.sessions s
        JOIN app.v_coach_public cp
            ON cp.user_id = s.coach_id
        LEFT JOIN app.session_participation sp
            ON sp.session_id = s.id
        LEFT JOIN app.user_profiles up
            ON up.user_id = sp.user_id
        WHERE EXISTS (
            SELECT 1
                FROM app.session_participation sp2
                WHERE sp2.session_id = s.id
                    AND sp2.user_id = :user_id
        )
        GROUP BY
            s.id,
            cp.user_id,
            cp.first_name,
            cp.last_name,
            s.title,
            s.starts_at,
            s.ends_at,
            s.status,
            s.cancelled_at,
            s.price_cents,
            s.currency,
            s.created_at,
            s.updated_at
        OFFSET :offset
        LIMIT :limit
        """)

        rows = await self._session.execute(stmt, {
            "user_id": user_id,
            "from_ts": _from,
            "to_ts": to,
            "offset": offset,
            "limit": limit + 1
        })

        rows = rows.mappings().all()
        has_more = len(rows) > limit

        rows = rows[:limit]

        print(rows)
        return [
            SessionCompleteEntity(
                id=row["id"],
                coach=UserProfileEntity(
                    user_id=row["user_id"],
                    first_name=row["first_name"],
                    last_name=row["last_name"]
                ),
                title=row["title"],
                starts_at=row["starts_at"],
                ends_at=row["ends_at"],
                status=row["status"],
                cancelled_at=row["cancelled_at"],
                price_cents=row["price_cents"],
                currency=row["currency"],
                created_at=row["created_at"],
                updated_at=row["updated_at"],
                participants=[UserProfileEntity(
                    user_id=participant["user_id"],
                    first_name=participant["first_name"],
                    last_name=participant["last_name"]
                    ) for participant in row["participants"]
                ]
            ) for row in rows
        ], has_more
