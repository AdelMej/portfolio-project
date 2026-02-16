from sqlalchemy.exc import DBAPIError
from sqlalchemy.sql.expression import text
from app.domain.auth.auth_exceptions import PermissionDeniedError
from app.domain.session.session_entity import NewSessionEntity
from sqlalchemy.ext.asyncio.session import AsyncSession
from app.feature.session.repositories.session_creation_repository_port import (
    SessionCreationRepoPort
)
from uuid import uuid4

from app.shared.database.sqlstate_extractor import get_sqlstate


class SqlAlchemySessionCreationRepo(SessionCreationRepoPort):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create_session(
        self,
        session: NewSessionEntity
    ) -> None:
        stmt = text("""
                SELECT
                    app_fcn.session_create_session(
                        :id,
                        :coach_id,
                        :title,
                        :starts_at,
                        :ends_at,
                        :price_cents,
                        :currency
                    )
            """)
        try:
            await self._session.execute(stmt, {
                    "id": uuid4(),
                    "coach_id": session.coach_id,
                    "title": session.title,
                    "starts_at": session.starts_at,
                    "ends_at": session.ends_at,
                    "price_cents": session.price_cents,
                    "currency": session.currency
                }
            )
        except DBAPIError as exc:
            code = get_sqlstate(exc)

            if code == "AP401":
                raise PermissionDeniedError() from exc

            raise
