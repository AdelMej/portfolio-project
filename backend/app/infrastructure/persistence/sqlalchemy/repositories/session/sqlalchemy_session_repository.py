from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID, uuid4
from typing import Optional

from app.domain.session.session_entity import SessionEntity
from sqlalchemy import text

class SqlAlchemySessionRepository:

    def __init__(self, session: AsyncSession):
        self.session = session

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
                "status": session.status
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
