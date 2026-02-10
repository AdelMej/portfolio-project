from sqlalchemy.ext.asyncio.session import AsyncSession
from app.feature.credit.uow.credit_uow_port import (
    CreditUoWPort
)
from app.infrastructure.persistence.sqlalchemy.repositories.credit import (
    SqlAlchemyCreditReadRepository
)


class SqlAlchemyCreditUoW(CreditUoWPort):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self.credit_read_repository = SqlAlchemyCreditReadRepository(session)
