from datetime import datetime

from app.domain.auth.actor_entity import Actor
from app.domain.auth.auth_exceptions import (
    AuthUserIsDisabledError,
    CoachNotFoundError
)
from app.domain.session.session_exception import (
    SessionCancelledError,
    SessionNotAttendedError,
    SessionNotFoundError,
    SessionStartedError
)
from app.feature.admin.session.admin_session_dto import (
    AdminSessionOutputDTO,
    UserProfileOutputDTO
)
from app.feature.admin.session.uow.admin_session_system_uow_port import (
    AdminSessionSystemUoWPort
)
from app.feature.admin.session.uow.admin_session_uow_port import (
    AdminSessionUoWPort
)
from uuid import UUID
from app.domain.auth.permission import Permission
from app.domain.auth.permission_rules import (
    ensure_has_permission
)


class AdminSessionService:
    async def admin_list_all_sessions(
        self,
        uow: AdminSessionUoWPort,
        actor: Actor,
        limit: int,
        offset: int,
        _from: datetime | None,
        to: datetime | None
    ) -> tuple[list[AdminSessionOutputDTO], bool]:
        ensure_has_permission(actor, Permission.ADMIN_READ_SESSION)

        if await uow.auth_read_repo.is_user_disabled(actor.id):
            raise AuthUserIsDisabledError()

        sessions, has_more = await uow.session_read_repo.get_all_sessions(
            limit=limit,
            offset=offset,
            _from=_from,
            to=to,
        )

        return [
            AdminSessionOutputDTO(
                id=s.id,
                coach_id=s.coach_id,
                title=s.title,
                starts_at=s.starts_at,
                ends_at=s.ends_at,
                status=s.status,
                cancelled_at=s.cancelled_at,
                price_cents=s.price_cents,
                currency=s.currency,
                created_at=s.created_at,
                updated_at=s.updated_at
            ) for s in sessions
        ], has_more

    async def admin_list_sessions_by_coach(
        self,
        uow: AdminSessionUoWPort,
        actor: Actor,
        coach_id: UUID,
        limit: int,
        offset: int,
        _from: datetime | None,
        to: datetime | None
    ) -> tuple[list[AdminSessionOutputDTO], bool]:
        ensure_has_permission(actor, Permission.ADMIN_READ_SESSION)

        if await uow.auth_read_repo.is_user_disabled(actor.id):
            raise AuthUserIsDisabledError()

        if not await uow.auth_read_repo.exists_coach(coach_id=coach_id):
            raise CoachNotFoundError()

        sessions, has_more = await uow.session_read_repo.sessions_by_coach_id(
            coach_id,
            limit,
            offset,
            _from,
            to
        )

        return [
            AdminSessionOutputDTO(
                id=s.id,
                coach_id=s.coach_id,
                title=s.title,
                starts_at=s.starts_at,
                ends_at=s.ends_at,
                status=s.status,
                cancelled_at=s.cancelled_at,
                price_cents=s.price_cents,
                currency=s.currency,
                created_at=s.created_at,
                updated_at=s.updated_at
            )
            for s in sessions
        ], has_more

    async def admin_cancel_session(
            self,
            uow: AdminSessionSystemUoWPort,
            actor: Actor,
            session_id: UUID
    ):
        ensure_has_permission(actor, Permission.ADMIN_CANCEL_SESSION)

        if await uow.auth_read_repo.is_user_disabled(actor.id):
            raise AuthUserIsDisabledError()

        if not await uow.session_read_repo.exist_session(session_id):
            raise SessionNotFoundError()

        if await uow.session_read_repo.is_session_cancelled(session_id):
            raise SessionCancelledError()

        if await uow.session_read_repo.is_session_started(
            session_id=session_id
        ):
            raise SessionStartedError()

        await uow.session_update_repo.cancel_session(session_id)

    async def admin_get_attendance_list(
        self,
        session_id: UUID,
        actor: Actor,
        uow: AdminSessionSystemUoWPort,
    ) -> list[UserProfileOutputDTO]:
        ensure_has_permission(actor, Permission.ADMIN_READ_ATTENDANCE)

        if not await uow.session_read_repo.exist_session(session_id):
            raise SessionNotFoundError()

        if not await (
            uow.session_attendance_read_repo.is_session_attended(session_id)
        ):
            raise SessionNotAttendedError()

        profiles = (
            await uow.session_attendance_read_repo.get_session_attendance_list(
                session_id=session_id
            )
        )

        return [
            UserProfileOutputDTO(
                user_id=profile.user_id,
                first_name=profile.first_name,
                last_name=profile.last_name,
                attended=profile.attended
            ) for profile in profiles
        ]
