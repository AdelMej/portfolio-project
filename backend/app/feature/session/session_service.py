from uuid import UUID
from fastapi import HTTPException
from datetime import datetime, timezone

from app.domain.session.session_creation_rules import (
    ensure_price_is_not_negative,
    ensure_times_valid,
    ensure_title_is_valid
)
from app.domain.session.session_status import SessionStatus
from app.feature.session.session_dto import (
    GetOutputDto,
    SessionUpdateInputDTO,
    AttendanceOutputDto,
    SessionCreationInputDTO
)
from app.domain.auth.actor_entity import Actor
from app.domain.auth.permission_rules import ensure_has_permission
from app.domain.auth.permission import Permission
from app.feature.session.uow.session_public_uow_port import (
    SessionPulbicUoWPort
)
from app.feature.session.uow.session_uow_port import SessionUoWPort
from app.domain.session.session_entity import NewSessionEntity
from app.shared.exceptions.commons import NotFoundError
from app.domain.currency.currency_rules import (
    ensure_currency_is_valid
)


class SessionService:
    async def get_session(
            self,
            uow: SessionPulbicUoWPort,
            session_id: UUID
    ) -> GetOutputDto:
        session = (
            await uow.session_read_repository.get_session_by_id(session_id)
        )

        if not session:
            raise NotFoundError()

        return GetOutputDto(
            id=session.id,
            coach_id=session.coach_id,
            title=session.title,
            starts_at=session.starts_at,
            ends_at=session.ends_at,
            status=session.status
        )

    async def create_session(
            self,
            uow: SessionUoWPort,
            actor: Actor,
            input: SessionCreationInputDTO
    ) -> None:
        ensure_has_permission(actor, Permission.CREATE_SESSION)

        # normalization
        title = input.title.strip()
        currency = input.currency.strip().upper()

        ensure_times_valid(input.starts_at, input.ends_at)
        ensure_price_is_not_negative(input.price_cents)
        ensure_title_is_valid(title)
        ensure_currency_is_valid(currency)

        new_session = NewSessionEntity(
            coach_id=actor.id,
            title=title,
            starts_at=input.starts_at,
            ends_at=input.ends_at,
            price_cents=input.price_cents,
            currency=currency
        )

        await uow.session_creation_repository.create_session(new_session)

    async def get_all_sessions(
        self,
        offset: int,
        limit: int,
        _from: datetime | None,
        to: datetime | None,
        uow: SessionPulbicUoWPort
    ) -> tuple[list[GetOutputDto], bool]:
        sessions, has_more = (
            await uow.session_read_repository.get_all_sessions(
                offset=offset,
                limit=limit,
                _from=_from,
                to=to,
            )
        )

        return [
            GetOutputDto(
                id=session.id,
                coach_id=session.coach_id,
                title=session.title,
                starts_at=session.starts_at,
                ends_at=session.ends_at,
                status=session.status
            )
            for session in sessions
        ], has_more

    async def get_sessions_by_coach(
        self,
        coach_id: UUID,
        offset: int,
        limit: int,
        _from: datetime | None,
        to: datetime | None,
        uow: SessionPulbicUoWPort
    ) -> tuple[list[GetOutputDto], bool]:
        sessions, has_more = (
            await uow.session_read_repository.get_sessions_by_coach_id(
                coach_id=coach_id,
                offset=offset,
                limit=limit,
                _from=_from,
                to=to,
            )
        )

        return [
            GetOutputDto(
                id=session.id,
                coach_id=session.coach_id,
                title=session.title,
                starts_at=session.starts_at,
                ends_at=session.ends_at,
                status=session.status
            )
            for session in sessions
        ], has_more

    async def cancel_session(
        self,
        uow,
        actor: Actor,
        session_id: UUID
    ):
        ensure_has_permission(actor, Permission.CANCEL_SESSION)

        session = await uow.session_repo.get_session_by_id(session_id)
        if not session:
            raise NotFoundError()

        if session.coach_id != actor.id:
            raise HTTPException(status_code=403, detail="Not your session")

        await uow.session_repo.cancel_session(session_id)

    async def get_attendance(
            self,
            uow: SessionUoWPort,
            actor: Actor,
            session_id: UUID
    ) -> AttendanceOutputDto:
        ensure_has_permission(actor, Permission.READ_SELF)

        session = await uow.session_repo.get_session_by_id(session_id)
        if not session:
            raise NotFoundError()

        if session.status == SessionStatus.CANCELLED:
            raise HTTPException(status_code=400, detail="Session cancelled")

        return await uow.session_repo.get_attendance(session_id)

    async def put_attendance(
            self,
            UoW,
            actor,
            session_id: UUID
    ) -> None:
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

    async def update_session(
            self,
            UoW: SessionUoWPort,
            actor: Actor,
            session_id: UUID,
            payload: SessionUpdateInputDTO
    ):
        ensure_has_permission(actor, Permission.CREATE_SESSION)

        session = await UoW.session_repo.get_session_by_id(session_id)
        if not session:
            raise NotFoundError()

        if session.coach_id != actor.id:
            raise HTTPException(status_code=403, detail="Not your session")

        now = datetime.now(timezone.utc)

        updated_session = session.update(
            title=payload.title,
            starts_at=payload.starts_at,
            ends_at=payload.ends_at,
            now=now,
        )

        await UoW.session_repo.update_session(updated_session)

    async def cancel_registration(
        self,
        uow,
        actor: Actor,
        session_id: UUID
    ):
        ensure_has_permission(actor, Permission.READ_SELF)

        session = await uow.session_repo.get_session_by_id(session_id)
        if not session:
            raise NotFoundError()

        if session.status == SessionStatus.CANCELLED:
            raise HTTPException(status_code=400, detail="Session cancelled")

        already_registered = await uow.session_repo.is_user_registered(
            session_id=session_id,
            user_id=actor.id
        )

        if not already_registered:
            raise HTTPException(status_code=409, detail="Not registered")

        removed = await uow.session_repo.remove_attendance(
            session_id=session_id,
            user_id=actor.id
        )

        if not removed:
            raise HTTPException(
                status_code=500,
                detail="Failed to cancel registration"
            )

    async def admin_list_sessions_by_coach(
            self,
            uow: SessionUoWPort,
            actor: Actor,
            coach_id: UUID
    ):
        ensure_has_permission(actor, Permission.READ_USERS)

        sessions = await uow.session_repo.list_sessions(coach_id=coach_id)

        return [
            GetOutputDto(
                id=s.id,
                coach_id=s.coach_id,
                title=s.title,
                starts_at=s.starts_at,
                ends_at=s.ends_at,
                status=s.status
            )
            for s in sessions
        ]

    async def admin_cancel_session(
            self,
            uow: SessionUoWPort,
            actor: Actor,
            session_id: UUID
    ):
        # Ensure admin permission
        ensure_has_permission(actor, Permission.READ_USERS)

        session = await uow.session_repo.get_session_by_id(session_id)
        if not session:
            raise NotFoundError()

        await uow.session_repo.cancel_session(session_id)
