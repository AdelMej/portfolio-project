from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID, uuid4
from typing import Optional

from app.infrastructure.persistence.sqlalchemy.models.sessions import Session as SessionModel
from app.domain.session.session_entity import SessionEntity
from sqlalchemy import text

class SqlAlchemySessionRepository:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_session_by_id(
        self,
        db: AsyncSession,
        session_id: UUID
    ) -> Optional[SessionModel]:
        return await db.get(SessionModel, session_id)

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

    async def list_sessions(self, db: AsyncSession, coach_id=None):
        from sqlalchemy import select
        stmt = select(SessionModel)
        if coach_id:
            stmt = stmt.where(SessionModel.coach_id == coach_id)

        result = await db.execute(stmt)
        return result.scalars().all()
