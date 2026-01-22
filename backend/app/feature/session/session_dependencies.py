from app.feature.session.session_service import SessionService
from app.feature.session.session_repository import (SessionRepository)
from app.infrastructure.persistence.provider import get_session_repository
from fastapi import Depends

def get_session_service(repo: SessionRepository = Depends (get_session_repository))->SessionService:
    return SessionService(repo)
