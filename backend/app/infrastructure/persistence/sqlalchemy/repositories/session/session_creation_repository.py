from sqlalchemy.sql.expression import text
from app.domain.session.session_entity import NewSessionEntity
from sqlalchemy.ext.asyncio.session import AsyncSession
from app.feature.session.repositories.session_creation_repository_port import (
    SessionCreationRepoPort
)
from uuid import UUID, uuid4
import json


class SqlAlchemySessionCreationRepo(SessionCreationRepoPort):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create_session(
        self,
        session: NewSessionEntity
    ) -> None:
        await self._session.execute(
            text("""
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
            """),
            {
                "id": uuid4(),
                "coach_id": session.coach_id,
                "title": session.title,
                "starts_at": session.starts_at,
                "ends_at": session.ends_at,
                "price_cents": session.price_cents,
                "currency": session.currency
            }
        )

    async def create_attendance(
        self,
        session_id: UUID,
        attendance_list: dict[UUID, bool]
    ) -> None:
        payload = [
            {
                "user_id": str(user_id),
                "attended": attended
            }
            for user_id, attended in attendance_list.items()
        ]

        await self._session.execute(
            text("""
                :session_id,
                :attendance_list
            """),
            {
                "session_id": session_id,
                "attendance_list": json.dumps(payload)
            }
        )
