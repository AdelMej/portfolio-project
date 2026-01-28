from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.feature.session.session_dto import SessionCreateRequest

from app.feature.session.session_service import SessionService
from app.feature.session.session_dependencies import get_session_service
from app.infrastructure.settings.provider import get_app_system_session
from app.feature.session.session_dto import GetOutputDto
from uuid import UUID

router = APIRouter()

@router.get("/{session_id}", response_model=GetOutputDto)
async def get_session(
    session_id: UUID,
    db: AsyncSession = Depends(get_app_system_session),
    service: SessionService = Depends(get_session_service)
):
    return await service.get_session(db, session_id)

# Added session coach

@router.post("/", response_model=GetOutputDto)
async def create_session(
    payload: SessionCreateRequest,
    db: AsyncSession = Depends(get_app_system_session),
    service: SessionService = Depends(get_session_service)
):
    coach_id = UUID("FAKE_FOR_NOW")  # auth later
    return await service.create_session(db, coach_id, payload)