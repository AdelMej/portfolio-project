from uuid import UUID
from fastapi import APIRouter

from app.domain.auth.actor_entity import Actor
from app.feature.admin.session.admin_session_service import AdminSessionService
from app.feature.admin.session.uow.admin_session_uow_port import AdminSessionUoWPort
from app.infrastructure.security.provider import get_current_actor

router = APIRouter(
    prefix='/admin/sessions',
    tags=["admin-session"]
)

@router.get(
    "/admin/sessions/{coach_id}",
    response_model=list[GetOutputDto]
)
async def admin_get_sessions_by_coach(
    coach_id: UUID,
    actor: Actor = Depends(get_current_actor),
    UoW: AdminSessionUoWPort = Depends(get_session_uow),
    service: AdminSessionService = Depends(get_session_service),
):
    return await service.admin_list_sessions_by_coach(UoW, actor, coach_id)


@router.put(
    "/admin/sessions/{session_id}/cancel",
    status_code=status.HTTP_204_NO_CONTENT
)
async def admin_cancel_session(
    session_id: UUID,
    actor: Actor = Depends(get_current_actor),
    UoW: AdminSessionService = Depends(get_session_uow),
    service: AdminSessionService = Depends(get_session_service),
):
    await service.admin_cancel_session(UoW, actor, session_id)
