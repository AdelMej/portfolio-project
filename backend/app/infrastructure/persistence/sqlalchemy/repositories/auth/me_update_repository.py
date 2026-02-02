from uuid import UUID
from sqlalchemy import text
from sqlalchemy.ext.asyncio.session import AsyncSession
from app.feature.auth.repositories.me_update_repository_port import (
    MeUpdateRepositoryPort
)


class SqlAlchemyMeUpdateRepository(MeUpdateRepositoryPort):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def update_email_by_user_id(self, email: str, user_id: UUID):
        await self._session.execute(
            text(
                """
                UPDATE app.users
                SET email = :email
                WHERE users.id = :user_id
                """
            ),
            {
                "email": email,
                "user_id": user_id
            }
        )
