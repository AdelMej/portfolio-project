from datetime import datetime
from fastapi import APIRouter, Depends, Query, status
from uuid import UUID
from app.feature.session.session_dto import (
    AttendanceOutputDto,
    SessionCreationInputDTO,
    GetOutputDto
)
from app.feature.session.session_service import SessionService
from app.feature.session.session_dependencies import get_session_service
from app.domain.auth.actor_entity import Actor
from app.feature.session.uow.session_public_uow_port import (
    SessionPulbicUoWPort
)
from app.infrastructure.security.provider import get_current_actor
from app.infrastructure.persistence.sqlalchemy.provider import (
    get_session_public_uow,
    get_session_uow
)
from app.feature.session.uow.session_uow_port import SessionUoWPort

router = APIRouter()


@router.get(
    "/{session_id}",
    status_code=200
)
async def get_session(
    session_id: UUID,
    uow: SessionPulbicUoWPort = Depends(get_session_public_uow),
    service: SessionService = Depends(get_session_service)
) -> GetOutputDto:
    return await service.get_session(
        uow=uow,
        session_id=session_id
    )


@router.post(
    "/",
    status_code=201
)
async def create_session(
    payload: SessionCreationInputDTO,
    actor: Actor = Depends(get_current_actor),
    UoW: SessionUoWPort = Depends(get_session_uow),
    service: SessionService = Depends(get_session_service)
) -> None:
    await service.create_session(UoW, actor, payload)


@router.get("/", response_model=list[GetOutputDto])
async def list_sessions(
    limit: int = Query(20, ge=0, le=100),
    offset: int = Query(0, ge=0),
    _from: datetime | None = Query(None),
    to: datetime | None = Query(None),
    UoW: SessionUoWPort = Depends(get_session_uow),
    service: SessionService = Depends(get_session_service)
):
    return await service.list_sessions(UoW)


@router.put(
    "/{session_id}",
    status_code=204
)
async def update_session(
    session_id: UUID,
    payload: SessionCreationInputDTO,
    actor: Actor = Depends(get_current_actor),
    UoW: SessionUoWPort = Depends(get_session_uow),
    service: SessionService = Depends(get_session_service)
):
    await service.update_session(UoW, actor, session_id, payload)


@router.put(
    "/{session_id}/cancel",
    status_code=status.HTTP_204_NO_CONTENT
)
async def cancel_session(
    session_id: UUID,
    actor: Actor = Depends(get_current_actor),
    UoW: SessionUoWPort = Depends(get_session_uow),
    service: SessionService = Depends(get_session_service),
):
    await service.cancel_session(UoW, actor, session_id)


@router.get(
    "/{session_id}/attendance",
    response_model=list[AttendanceOutputDto]
)
async def get_attendance(
    session_id: UUID,
    actor: Actor = Depends(get_current_actor),
    UoW: SessionUoWPort = Depends(get_session_uow),
    service: SessionService = Depends(get_session_service),
):
    return await service.get_attendance(UoW, actor, session_id)


@router.put(
    "/{session_id}/attendance",
    status_code=204
)
async def put_attendance(
    session_id: UUID,
    actor: Actor = Depends(get_current_actor),
    UoW: SessionUoWPort = Depends(get_session_uow),
    service: SessionService = Depends(get_session_service),
):
    """
    Register the current actor as attending the session.
    """
    await service.put_attendance(UoW, actor, session_id)


@router.post(
    "/sessions/{session_id}/cancel-registration",
    status_code=204
)
async def cancel_registration(
    session_id: UUID,
    actor: Actor = Depends(get_current_actor),
    UoW: SessionUoWPort = Depends(get_session_uow),
    service: SessionService = Depends(get_session_service),
):
    await service.cancel_registration(UoW, actor, session_id)


@router.get(
    "/admin/sessions/{coach_id}",
    response_model=list[GetOutputDto]
)
async def admin_get_sessions_by_coach(
    coach_id: UUID,
    actor: Actor = Depends(get_current_actor),
    UoW: SessionUoWPort = Depends(get_session_uow),
    service: SessionService = Depends(get_session_service),
):
    return await service.admin_list_sessions_by_coach(UoW, actor, coach_id)


@router.put(
    "/admin/sessions/{session_id}/cancel",
    status_code=status.HTTP_204_NO_CONTENT
)
async def admin_cancel_session(
    session_id: UUID,
    actor: Actor = Depends(get_current_actor),
    UoW: SessionUoWPort = Depends(get_session_uow),
    service: SessionService = Depends(get_session_service),
):
    await service.admin_cancel_session(UoW, actor, session_id)
