from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID, uuid4
from typing import Optional

from app.domain.session.session_entity import SessionEntity
from sqlalchemy import text

class SqlAlchemySessionRepository:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_session_by_id(
        self,
        session_id: UUID
    ) -> Optional [SessionEntity]:
        result= await self.session.execute(
            text(
                """SELECT
                    id,
                    coach_id,
                    title,
                    starts_at,
                    ends_at,
                    status::text
                FROM app.sessions
                WHERE id=:id
                """
            ),
            {
                'id':session_id
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
            status=row["status"]
        )

    async def create_session(
        self,
        session: SessionEntity
    ) -> SessionEntity:
        session_id = uuid4()
        await self.session.execute(
            text(
                """INSERT INTO app.sessions(
                    id,
                    coach_id,
                    title,
                    starts_at,
                    ends_at,
                    status
                ) VALUES (
                    :id,
                    :coach_id,
                    :title,
                    :starts_at,
                    :ends_at,
                    :status
                )
                """
            ), 
            {
                'id':str(session_id), 
                'coach_id':str(session.coach_id),
                'title': session.title,
                'starts_at': session.starts_at,
                'ends_at': session.ends_at,
                'status': session.status
            }
        )

        return session

    async def list_sessions(self, coach_id: UUID | None = None):
        if coach_id:
            res = await self.session.execute(
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
        else:
            res = await self.session.execute(
                text("""SELECT
                        id,
                        coach_id,
                        title,
                        starts_at,
                        ends_at,
                        status::text
                   FROM app.sessions
                """)
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


    async def cancel_session(self, session_id: UUID) -> bool:
        result = await self.session.execute(
                text("""
                    UPDATE app.sessions
                    SET status = 'cancelled',
                        cancelled_at = now()
                    WHERE id = :id
                """),
                {"id": session_id},
            )
        return result.rowcount > 0

    async def get_attendance(self, session_id: UUID) -> list[UUID]:
        result = await self.session.execute(
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
    
    #List attendances

    async def is_user_registered(self, session_id: UUID, user_id: UUID) -> bool:
        result = await self.session.execute(
            text(
                """
                SELECT 1
                FROM app.session_attendance
                WHERE session_id = :session_id
                AND user_id = :user_id
                """
            ),
            {"session_id": session_id, "user_id": user_id}
        )
        row = result.first()
        return row is not None

    async def add_attendance(self, session_id: UUID, user_id: UUID) -> None:
        await self.session.execute(
            text("""
                INSERT INTO app.session_attendance (session_id, user_id)
                VALUES (:session_id, :user_id)
            """),
            {
                "session_id": session_id,
                "user_id": user_id,
            }
        )

    async def update_session(self, session: SessionEntity) -> SessionEntity:
        """
        Update a session in the database using the SessionEntity.
        """
        await self.session.execute(
            text(
                """
                UPDATE app.sessions
                SET
                    title = :title,
                    starts_at = :starts_at,
                    ends_at = :ends_at,
                    status = :status
                WHERE id = :id
                """
            ),
            {
                "id": str(session.id),
                "title": session.title,
                "starts_at": session.starts_at,
                "ends_at": session.ends_at,
                "status": session.status.value if hasattr(session.status, "value") else session.status
            }
        )

        return session
    
    async def remove_attendance(self, session_id: UUID, user_id: UUID) -> bool:
        result = await self.session.execute(
            text("""
                DELETE FROM app.session_attendance
                WHERE session_id = :session_id
                  AND user_id = :user_id
            """),
            {
                "session_id": session_id,
                "user_id": user_id
            }
        )
        return result.rowcount > 0
