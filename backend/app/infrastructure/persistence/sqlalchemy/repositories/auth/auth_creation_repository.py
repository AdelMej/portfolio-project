from uuid import uuid4
from sqlalchemy import text
from sqlalchemy.ext.asyncio.session import AsyncSession
from app.domain.user.user_entity import NewUserEntity
from app.domain.user.user_profile_entity import NewUserProfileEntity
from app.feature.auth.repositories.auth_creation_respository_port import (
    AuthCreationRepositoryPort
)


class SqlAlchemyAuthCreationRepository(AuthCreationRepositoryPort):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def register(
            self,
            user: NewUserEntity,
            user_profile: NewUserProfileEntity
    ) -> None:

        id = uuid4()

        await self._session.execute(
            text("""
                SELECT
                    app_fcn.register_user(
                        :id,
                        :email,
                        :password_hash,
                        :first_name,
                        :last_name,
                        :role_name
                    )
            """),
            {
                "id": id,
                "email": user.email,
                "password_hash": user.password_hash,
                "first_name": user_profile.first_name,
                "last_name": user_profile.last_name,
                "role_name": user.role.value
             }
        )
