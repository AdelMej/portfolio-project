from uuid import UUID
from sqlalchemy import text
from sqlalchemy.ext.asyncio.session import AsyncSession
from app.feature.auth.repositories.me_update_repository_port import (
    MeUpdateRepoPort
)


class SqlAlchemyMeUpdateRepo(MeUpdateRepoPort):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def update_email_by_user_id(self, email: str, user_id: UUID):
        await self._session.execute(
            text(
                """
                SELECT
                    app_fcn.me_change_email(:user_id, :email)
                """
            ),
            {
                "email": email,
                "user_id": user_id
            }
        )

    async def update_password_by_id(self, user_id: UUID, password_hash: str):
        await self._session.execute(
            text("""
                SELECT
                    app_fcn.me_change_password(:user_id, :password_hash)
            """),
            {
                "password_hash": password_hash,
                "user_id": user_id
            }
        )

    async def update_profile_by_id(
        self,
        user_id: UUID,
        first_name: str,
        last_name: str
    ):

        await self._session.execute(
            text("""
                UPDATE app.user_profiles up
                SET
                    first_name = :first_name,
                    last_name = :last_name
                WHERE up.user_id = :user_id
            """),
            {
                "first_name": first_name,
                "last_name": last_name,
                "user_id": user_id
            }
        )
