from datetime import datetime
from uuid import UUID
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.sql import text
from app.domain.session.session_entity import (
    SessionCompleteEntity,
)
from app.domain.session.session_status import SessionStatus
from app.domain.user.user_profile_entity import UserProfileEntity
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
        WHERE cp.user_id = :coach_id
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

        res = await self._session.execute(stmt, {
            "coach_id": coach_id,
            "offset": offset,
            "limit": limit
        })

        rows = res.mappings().all()
        has_more = len(rows) > limit
        rows[:limit]

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
                status=SessionStatus(row["status"]),
                cancelled_at=row["cancelled_at"],
                price_cents=row["price_cents"],
                currency=row["currency"],
                created_at=row["created_at"],
                updated_at=row["updated_at"],
                participants=[
                    UserProfileEntity(
                        user_id=participant["user_id"],
                        first_name=participant["first_name"],
                        last_name=participant["last_name"]
                    ) for participant in row["participants"]
                ]
            ) for row in rows
        ], has_more

    async def get_all_sessions(
        self,
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

        res = await self._session.execute(stmt, {
            "offset": offset,
            "limit": limit
        })

        rows = res.mappings().all()
        has_more = len(rows) > limit
        rows[:limit]

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
                status=SessionStatus(row["status"]),
                cancelled_at=row["cancelled_at"],
                price_cents=row["price_cents"],
                currency=row["currency"],
                created_at=row["created_at"],
                updated_at=row["updated_at"],
                participants=[
                    UserProfileEntity(
                        user_id=participant["user_id"],
                        first_name=participant["first_name"],
                        last_name=participant["last_name"]
                    ) for participant in row["participants"]
                ]
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

    async def get_session_participants(
        self,
        session_id: UUID
    ) -> list[tuple[str, str]]:
        res = await self._session.execute(
            text("""
                SELECT up.first_name, up.last_name
                FROM app.session_participation sp
                JOIN app.user_profiles up ON up.user_id = sp.user_id
                WHERE sp.session_id = :session_id
                ORDER BY up.last_name, up.first_name
            """),
            {"session_id": session_id}
        )
        rows = res.all()
        return [(r[0], r[1]) for r in rows]
