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

    async def list_sessions(self, coach_id: UUID):
        res = await self._session.execute(
            text("""SELECT
                        id,
                        coach_id,
                        title,
                        starts_at,
                        ends_at,
                        status::text
                   FROM app.sessions
                   WHERE coach_id = :coach_id
                """),
            {"coach_id": coach_id}
        )

        rows = res.mappings().all()
        return [
            SessionEntity(
                id=row["id"],
                coach_id=row["coach_id"],
                title=row["title"],
                starts_at=row["starts_at"],
                ends_at=row["ends_at"],
                status=row["status"]
            )
            for row in rows
        ]

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
