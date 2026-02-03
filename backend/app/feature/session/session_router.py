from fastapi import APIRouter, Depends
from uuid import UUID

from app.feature.session.session_dto import SessionCreateRequest, GetOutputDto
from app.feature.session.session_service import SessionService
from app.feature.session.session_dependencies import get_session_service
from app.domain.auth.actor_entity import Actor
from app.infrastructure.security.provider import get_current_actor
from app.infrastructure.persistence.sqlalchemy.provider import get_session_uow
from app.feature.session.session_uow_port import SessionUoWPort

router = APIRouter()

@router.get("/{session_id}", response_model=GetOutputDto)
async def get_session(
    session_id: UUID,
    UoW: SessionUoWPort = Depends(get_session_uow),
    service: SessionService = Depends(get_session_service)
):
    return await service.get_session(UoW, session_id)


@router.post("/", status_code=204)
async def create_session(
    
    payload: SessionCreateRequest,
    actor : Actor = Depends(get_current_actor),
    UoW: SessionUoWPort = Depends(get_session_uow),
    service: SessionService = Depends(get_session_service)
):
    
    await service.create_session(UoW, actor, payload)


@router.get("/", response_model=list[GetOutputDto])
async def list_sessions(
    UoW: SessionUoWPort = Depends(get_session_uow),
    service: SessionService = Depends(get_session_service)
):
    return await service.list_sessions(UoW)
