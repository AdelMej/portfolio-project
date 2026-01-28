from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID

from app.infrastructure.persistence.sqlalchemy.models.sessions import Session as SessionModel


class SqlAlchemySessionRepo:

    async def get_session_by_id(
        self,
        db: AsyncSession,
        session_id: UUID
    ) -> SessionModel | None:

        query = select(SessionModel).where(SessionModel.id == session_id)
        result = await db.execute(query)
        return result.scalar_one_or_none()

    async def create_session(
        self,
        db: AsyncSession,
        session: SessionModel
    ) -> SessionModel:

        db.add(session)
        await db.commit()
        await db.refresh(session)
        return session

    async def list_sessions(
        self,
        db: AsyncSession,
        coach_id: UUID | None = None
    ) -> list[SessionModel]:

        query = select(SessionModel)

        if coach_id:
            query = query.where(SessionModel.coach_id == coach_id)

        result = await db.execute(query)
        return result.scalars().all()

    async def update_session(
        self,
        db: AsyncSession,
        session: SessionModel
    ) -> SessionModel:

        await db.commit()
        await db.refresh(session)
        return session
