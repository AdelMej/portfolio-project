from fastapi import Depends
from app.feature.session.session_uow_port import SessionUoWPort
from app.infrastructure.persistence.sqlalchemy.provider import get_session_uow
from app.feature.session.session_service import SessionService

def get_session_service(
    uow: SessionUoWPort = Depends(get_session_uow)
) -> SessionService:
    return SessionService(uow)
