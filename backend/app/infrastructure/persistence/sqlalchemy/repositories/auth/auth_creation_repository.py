from uuid import uuid4
from sqlalchemy import text
from sqlalchemy.ext.asyncio.session import AsyncSession
from app.domain.user.user_entity import NewUserEntity
from app.domain.user.user_profile_entity import UserProfileEntity
from app.feature.auth.repositories.auth_creation_respository_port import (
    AuthCreationRepositoryPort
)


class SqlAlchemyAuthCreationRepository(AuthCreationRepositoryPort):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def register(
            self,
            user: NewUserEntity,
            user_profile: UserProfileEntity
    ) -> None:

        id = uuid4()

        await self._session.execute(
            text("""
                INSERT INTO app.users(id, email, password_hash)
                VALUES(:id, :email, :password_hash)
            """),
            {
                "id": id,
                "email": user.email,
                "password_hash": user.password_hash
             }
        )

        await self._session.execute(
            text("""
                INSERT INTO app.user_profiles(user_id, first_name, last_name)
                VALUES(:id, :first_name, :last_name)
            """),
            {
                "id": id,
                "first_name": user_profile.first_name,
                "last_name": user_profile.last_name
            }
        )

        res = await self._session.execute(
            text("""
                SELECT roles.id
                FROM app.roles
                where roles.role_name = :role_name
            """),
            {"role_name": user.role.value}
        )

        role_id = res.scalar_one()

        await self._session.execute(
            text("""
                INSERT INTO app.user_roles(user_id, role_id)
                VALUES(:user_id, :role_id)
            """),
            {"user_id": id, "role_id": role_id}
        )
