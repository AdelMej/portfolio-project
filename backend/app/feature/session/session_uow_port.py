from typing import Protocol
from app.feature.session.session_repository import SessionRepository


class SessionUoWPort(Protocol):
    session_repo: SessionRepository