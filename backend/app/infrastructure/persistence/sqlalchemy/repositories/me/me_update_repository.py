from uuid import UUID
from sqlalchemy import text
from sqlalchemy.exc import DBAPIError
from sqlalchemy.ext.asyncio.session import AsyncSession
from app.domain.auth.auth_exceptions import (
    EmailAlreadyExistError,
    PasswordIsBlankError,
    PermissionDeniedError
)
from app.feature.auth.repositories.me_update_repository_port import (
    MeUpdateRepoPort
)
from app.shared.database.sqlstate_extractor import get_sqlstate


class SqlAlchemyMeUpdateRepo(MeUpdateRepoPort):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def update_email_by_user_id(self, email: str, user_id: UUID):
        stmt = text(
                """
                SELECT
                    app_fcn.me_change_email(:user_id, :email)
                """
            )
        try:
            await self._session.execute(stmt, {
                    "email": email,
                    "user_id": user_id
                }
            )
        except DBAPIError as exc:
            code = get_sqlstate(exc)

            if code == "AP401":
                raise PermissionDeniedError()

            if code == "AP400":
                raise EmailAlreadyExistError()

    async def update_password_by_id(self, user_id: UUID, password_hash: str):
        stmt = text("""
                SELECT
                    app_fcn.me_change_password(:user_id, :password_hash)
            """)

        try:
            await self._session.execute(stmt, {
                    "password_hash": password_hash,
                    "user_id": user_id
                }
            )
        except DBAPIError as exc:
            code = get_sqlstate(exc)

            if code == "AP401":
                raise PermissionDeniedError() from exc

            if code == "AP400":
                raise PasswordIsBlankError() from exc

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
