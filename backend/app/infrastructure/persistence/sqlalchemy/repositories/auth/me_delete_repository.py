from uuid import UUID
from sqlalchemy import text
from sqlalchemy.ext.asyncio.session import AsyncSession
from app.feature.auth.repositories.me_delete_repository_port import (
    MeDeleteRepositoryPort
)


class SqlAlchemyMeDeleteRepository(MeDeleteRepositoryPort):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def soft_delete_user(
            self,
            user_id: UUID,
    ) -> None:

        await self._session.execute(
            text("""
                SELECT
                    app_fcn.me_self_delete(:user_id)
            """),
            {
                "user_id": user_id
            }
        )
