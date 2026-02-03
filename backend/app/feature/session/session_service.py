from uuid import UUID, uuid4
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

from app.domain.session.session_status import SessionStatus
from app.feature.session.session_dto import GetOutputDto, SessionCreateRequest
from app.domain.auth.actor_entity import Actor
from app.domain.auth.permission_rules import ensure_has_permission
from app.domain.auth.permission import Permission
from app.feature.session.session_uow_port import SessionUoWPort
from app.domain.session.session_entity import SessionEntity
class SessionService:

    async def get_session(self, UoW: SessionUoWPort, session_id: UUID) -> GetOutputDto:
        session = await UoW.session_repo.get_session_by_id(session_id)

        if not session:
            raise HTTPException(status_code=404, detail="Session not found")

        return GetOutputDto(
            id=session.id,
            coach_id=session.coach_id,
            title=session.title,
            starts_at=session.starts_at,
            ends_at=session.ends_at,
            status=session.status.value if hasattr(session.status, "value") else session.status
        )

    async def create_session(self, UoW: SessionUoWPort , actor: Actor, request: SessionCreateRequest) -> GetOutputDto:
        ensure_has_permission(actor, Permission.CREATE_SESSION)
        if request.starts_at >= request.ends_at:
            raise HTTPException(status_code=400, detail="Start time must be before end time")
        
        new_session = SessionEntity(
            id=uuid4(),
            coach_id=actor.id,
            title=request.title,
            starts_at=request.starts_at,
            ends_at=request.ends_at,
            status=SessionStatus.SCHEDULED
        )

        await self._repo.session_repo.create_session(new_session)


    async def list_sessions(self, UoW: SessionUoWPort):
        sessions = await self._repo.session_repo.list_sessions(db)

        return [
            GetOutputDto(
                id=s.id,
                coach_id=s.coach_id,
                title=s.title,
                starts_at=s.starts_at,
                ends_at=s.ends_at,
                status=s.status.value if hasattr(s.status, "value") else s.status
            )
            for s in sessions
        ]