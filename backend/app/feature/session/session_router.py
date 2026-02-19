from datetime import datetime
from fastapi import APIRouter, Depends, Query, status
from uuid import UUID
from app.feature.session.session_dto import (
    AttendanceInputDTO,
    AttendanceOutputDto,
    PaginatedSessionsOutputDTO,
    RegistrationOutputDTO,
    SessionCreationInputDTO,
    GetOutputDto,
    SessionUpdateInputDTO
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
from app.infrastructure.settings.provider import get_session_participation_ttl

router = APIRouter(
    prefix="/sessions",
    tags=["sessions"]
)


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
    input: SessionCreationInputDTO,
    actor: Actor = Depends(get_current_actor),
    uow: SessionUoWPort = Depends(get_session_uow),
    service: SessionService = Depends(get_session_service)
):
    await service.create_session(
        uow,
        actor,
        input
    )

    return {"message": "session created successfully"}


@router.get(
    "/",
    response_model=PaginatedSessionsOutputDTO
)
async def get_all_sessions(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    _from: datetime | None = Query(None),
    to: datetime | None = Query(None),
    uow: SessionPulbicUoWPort = Depends(get_session_public_uow),
    service: SessionService = Depends(get_session_service)
) -> PaginatedSessionsOutputDTO:
    items, has_more = await service.get_all_sessions(
        offset=offset,
        limit=limit,
        _from=_from,
        to=to,
        uow=uow,
    )

    return PaginatedSessionsOutputDTO(
        items=items,
        limit=limit,
        offset=offset,
        has_more=has_more
    )


@router.put(
    "/{session_id}",
    status_code=204
)
async def update_session(
    session_id: UUID,
    input: SessionUpdateInputDTO,
    actor: Actor = Depends(get_current_actor),
    uow: SessionUoWPort = Depends(get_session_uow),
    service: SessionService = Depends(get_session_service)
):
    await service.update_session(
        uow,
        actor,
        session_id,
        input
    )


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
    input: AttendanceInputDTO,
    actor: Actor = Depends(get_current_actor),
    uow: SessionUoWPort = Depends(get_session_uow),
    service: SessionService = Depends(get_session_service),
):
    """
    Register the current actor as attending the session.
    """
    await service.put_attendance(
        input=input,
        uow=uow,
        actor=actor,
        session_id=session_id
    )


@router.post(
    "/{session_id}/cancel-registration",
    status_code=204
)
async def cancel_registration(
    session_id: UUID,
    actor: Actor = Depends(get_current_actor),
    uow: SessionUoWPort = Depends(get_session_uow),
    service: SessionService = Depends(get_session_service),
):
    await service.cancel_registration(uow, actor, session_id)


@router.post(
    "/{session_id}/register",
    status_code=201
)
async def register_user(
    session_id: UUID,
    actor: Actor = Depends(get_current_actor),
    uow: SessionUoWPort = Depends(get_session_uow),
    service: SessionService = Depends(get_session_service),
    session_ttl: int = Depends(get_session_participation_ttl)
) -> RegistrationOutputDTO:
    required_payment, key = await service.register_user(
        session_id=session_id,
        actor=actor,
        uow=uow,
        session_ttl=session_ttl
    )

    return RegistrationOutputDTO(
        payment_intent_client_secret=key,
        require_payment=required_payment
    )
