from app.feature.session.session_repository import (SessionRepository)
from app.infrastructure.persistence.sqlalchemy.repositories.sqlalchemy_session_repository import (SqlAlchemySessionRepo)

def get_session_repository() -> SessionRepository:
    return SqlAlchemySessionRepo()