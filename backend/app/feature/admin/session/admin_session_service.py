from app.domain.auth.actor_entity import Actor
from app.feature.admin.session.admin_session_dto import AdminSessionOutputDTO
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


class AdminSessionService():
    async def admin_list_sessions_by_coach(
            self,
            uow: AdminSessionUoWPort,
            actor: Actor,
            coach_id: UUID
    ) -> tuple[list[AdminSessionOutputDTO], bool]:
        ensure_has_permission(actor, Permission.READ_USERS)

        sessions, has_more = await uow.session_repo.list_sessions(coach_id)

        return [
            AdminSessionOutputDTO(
                id=s.id,
                coach_id=s.coach_id,
                title=s.title,
                starts_at=s.starts_at,
                ends_at=s.ends_at,
                status=s.status
            )
            for s in sessions
        ], has_more

    async def admin_cancel_session(
            self,
            uow: AdminSessionSystemUoWPort,
            actor: Actor,
            session_id: UUID
    ):
        # Ensure admin permission
        ensure_has_permission(actor, Permission.READ_USERS)

        session = await uow.session_repo.get_session_by_id(session_id)
        if not session:
            raise NotFoundError()

        await uow.session_repo.cancel_session(session_id)
