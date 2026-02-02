from sqlalchemy.ext.asyncio.session import AsyncSession
from app.infrastructure.persistence.sqlalchemy.repositories.auth import (
    SqlAlchemyAuthCreationRepository
)
from app.feature.auth.uow.registration_uow_port import RegistrationUoWPort


class SqlAlchemyRegistrationUoW(RegistrationUoWPort):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

        self.auth_creation = SqlAlchemyAuthCreationRepository(session)
