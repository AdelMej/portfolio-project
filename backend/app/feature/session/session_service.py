from uuid import UUID
from app.infrastructure.persistence.sqlalchemy.models.sessions import Session as SessionModel
from app.domain.session.session_status import SessionStatus
from app.feature.session.session_repository import SessionRepository
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from typing import List
from fastapi import HTTPException, status


from app.feature.session.session_dto import GetOutputDto

from app.feature.session.session_dto import SessionCreateRequest

class SessionService:

    def __init__(self, repo: SessionRepository) -> None:
        self._repo = repo

    async def get_session(self, db: AsyncSession, session_id: UUID) -> GetOutputDto:
        session = await self._repo.get_session_by_id(db, session_id)

        if not session:
            raise HTTPException(status_code=404, detail="Session not found")

        return GetOutputDto(
            id=session.id,
            coach_id=session.coach_id,
            title=session.title,
            starts_at=session.starts_at,
            ends_at=session.ends_at,
            status=session.status.value
        )

# Added session coach


    async def create_session(self, db: AsyncSession, coach_id: UUID, request: SessionCreateRequest):
        ensure_times_valid(request.starts_at, request.ends_at)

        new_session = SessionModel(
            id=uuid.uuid4(),
            coach_id=coach_id,
            title=request.title,
            starts_at=request.starts_at,
            ends_at=request.ends_at,
            status=SessionStatus.SCHEDULED
        )

        return await self._repo.create_session(db, new_session)