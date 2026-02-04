from uuid import UUID, uuid4
from fastapi import HTTPException

from app.domain.session.session_status import SessionStatus
from app.feature.session.session_dto import GetOutputDto, SessionCreateRequest
from app.domain.auth.actor_entity import Actor
from app.domain.auth.permission_rules import ensure_has_permission
from app.domain.auth.permission import Permission
from app.feature.session.session_uow_port import SessionUoWPort
from app.domain.session.session_entity import SessionEntity
from app.shared.exceptions.commons import NotFoundError


class SessionService:

    async def get_session(self, UoW: SessionUoWPort, session_id: UUID) -> GetOutputDto:
        session = await UoW.session_repo.get_session_by_id(session_id)

        if not session:
            raise NotFoundError()

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

        await UoW.session_repo.create_session(new_session)


    async def list_sessions(self, UoW: SessionUoWPort):
        sessions = await UoW.session_repo.list_sessions()

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

    async def cancel_session(self, UoW, actor, session_id):
        ensure_has_permission(actor, Permission.CANCEL_SESSION)

        session = await UoW.session_repo.get_session_by_id(session_id)
        if not session:
            raise NotFoundError()

        if session.coach_id != actor.id:
            raise HTTPException(status_code=403, detail="Not your session")

        await UoW.session_repo.cancel_session(session_id)


    async def get_attendance(self,UoW: SessionUoWPort,actor: Actor,session_id: UUID):
        ensure_has_permission(actor, Permission.READ_SELF)

        session = await UoW.session_repo.get_session_by_id(session_id)
        if not session:
            raise NotFoundError()

        if session.status == SessionStatus.CANCELLED:
            raise HTTPException(status_code=400, detail="Session cancelled")

        return await UoW.session_repo.get_attendance(session_id)
    

    async def put_attendance(self, UoW, actor, session_id: UUID):
        ensure_has_permission(actor, Permission.READ_SELF)

        # 1. Get the session
        session = await UoW.session_repo.get_session_by_id(session_id)
        if not session:
            raise NotFoundError()

        if session.status == SessionStatus.CANCELLED:
            raise HTTPException(status_code=400, detail="Session cancelled")

        # 2. Check if the user is an active participant
        is_participant = await UoW.session_repo.is_user_registered(
            session_id=session_id,
            user_id=actor.id
        )

        if not is_participant:
            raise HTTPException(
                status_code=403,
                detail="User is not an active participant for this session"
            )

        # 3. Check if attendance was already added
        already_registered = await UoW.session_repo.has_attendance(
            session_id=session_id,
            user_id=actor.id
        )

        if already_registered:
            raise HTTPException(status_code=409, detail="Already registered")

        # 4. Add attendance
        await UoW.session_repo.add_attendance(
            session_id=session_id,
            user_id=actor.id
        )