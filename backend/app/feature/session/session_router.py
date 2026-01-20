from fastapi import APIRouter, Depends
from app.feature.session.session_service import SessionService
from app.feature.session.session_dependencies import get_session_service
from app.feature.session.session_dto import SessionInputDTO

router = APIRouter()

@router.get("/")
async def get(dto : SessionInputDTO , service:SessionService = Depends(get_session_service)):
    print (dto.email, dto.firstName)
    return await service.get_session()
