from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.persistence.sqlalchemy.repositories.sqlalchemy_session_repository import (
    SqlAlchemySessionRepository
)

class SqlAlchemySessionUoW:
  
    def __init__(self, session: AsyncSession):
        self.session_repo = SqlAlchemySessionRepository(session)
        