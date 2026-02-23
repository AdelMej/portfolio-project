from datetime import datetime
from uuid import UUID
from fastapi import APIRouter, Depends, Query

from app.domain.auth.actor_entity import Actor
from app.feature.admin.session.admin_session_dependencies import (
    get_admin_session_service
)
from app.feature.admin.session.admin_session_dto import (
    PaginatedAdminSessionOutputDTO,
    UserProfileOutputDTO
)
from app.feature.admin.session.admin_session_service import (
    AdminSessionService
)
from app.feature.admin.session.uow.admin_session_system_uow_port import (
    AdminSessionSystemUoWPort
)
from app.feature.admin.session.uow.admin_session_uow_port import (
    AdminSessionUoWPort
)
from app.infrastructure.persistence.sqlalchemy.provider import (
    get_admin_session_system_uow,
    get_admin_session_uow
)
from app.infrastructure.security.provider import get_current_actor

router = APIRouter(
    prefix='/admin/sessions',
    tags=["admin-session"]
)


@router.get(
    path="/",
    response_model=PaginatedAdminSessionOutputDTO
)
async def admin_get_all_session(
    limit: int = Query(0, ge=0, le=100),
    offset: int = Query(0, ge=0),
    _from: datetime | None = Query(None),
    to: datetime | None = Query(None),
    uow: AdminSessionUoWPort = Depends(get_admin_session_uow),
    actor: Actor = Depends(get_current_actor),
    service: AdminSessionService = Depends(get_admin_session_service)
) -> PaginatedAdminSessionOutputDTO:
    items, has_more = await service.admin_list_all_sessions(
        uow=uow,
        actor=actor,
        limit=limit,
        offset=offset,
        _from=_from,
        to=to
    )

    return PaginatedAdminSessionOutputDTO(
        items=items,
        limit=limit,
        offset=offset,
        has_more=has_more
    )


@router.get(
    "/{coach_id}",
    response_model=PaginatedAdminSessionOutputDTO
)
async def admin_get_sessions_by_coach(
    coach_id: UUID,
    limit: int = Query(0, ge=0, le=100),
    offset: int = Query(0, ge=0),
    _from: datetime | None = Query(None),
    to: datetime | None = Query(None),
    actor: Actor = Depends(get_current_actor),
    uow: AdminSessionUoWPort = Depends(get_admin_session_uow),
    service: AdminSessionService = Depends(get_admin_session_service),
):
    items, has_more = await service.admin_list_sessions_by_coach(
        uow=uow,
        actor=actor,
        coach_id=coach_id,
        limit=limit,
        offset=offset,
        _from=_from,
        to=to
    )

    return PaginatedAdminSessionOutputDTO(
        items=items,
        limit=limit,
        offset=offset,
        has_more=has_more
    )


@router.put(
    "/{session_id}/cancel",
    status_code=204
)
async def admin_cancel_session(
    session_id: UUID,
    actor: Actor = Depends(get_current_actor),
    uow: AdminSessionSystemUoWPort = Depends(get_admin_session_system_uow),
    service: AdminSessionService = Depends(get_admin_session_service),
):
    await service.admin_cancel_session(
        uow=uow,
        actor=actor,
        session_id=session_id
    )


@router.get(
    path="/{session_id}/attendance",
    status_code=200
)
async def get_attendance_list(
    session_id: UUID,
    actor: Actor = Depends(get_current_actor),
    uow: AdminSessionSystemUoWPort = Depends(get_admin_session_system_uow),
    service: AdminSessionService = Depends(get_admin_session_service)
) -> list[UserProfileOutputDTO]:

    return await service.admin_get_attendance_list(
        session_id=session_id,
        actor=actor,
        uow=uow,
    )
