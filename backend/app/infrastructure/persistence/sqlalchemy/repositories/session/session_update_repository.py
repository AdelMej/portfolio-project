from datetime import datetime
from uuid import UUID
from sqlalchemy import text
from sqlalchemy.ext.asyncio.session import AsyncSession
from app.feature.session.repositories.session_update_repository_port import (
    SessionUpdateRepositoryPort
)


class SqlAlchemySessionUpdateRepository(SessionUpdateRepositoryPort):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def update_session(
        self,
        session_id: UUID,
        title: str,
        starts_at: datetime,
        ends_at: datetime
    ) -> None:
        await self._session.execute(
            text("""
                SELECT
                    app_fcn.session_update(
                        :session_id,
                        :title,
                        :starts_at,
                        :ends_at
                    )
            """),
            {
                "session_id": session_id,
                "title": title,
                "starts_at": starts_at,
                "ends_at": ends_at
            }
        )

    async def cancel_session(
            self,
            session_id: UUID
    ) -> bool:
        ...
