from sqlalchemy.ext.asyncio.session import AsyncSession
from app.feature.credit.uow.credit_uow_port import (
    CreditUoWPort
)
from app.infrastructure.persistence.sqlalchemy.repositories import (
    SqlAlchemyCreditLedgerReadRepo,
    SqlAlchemyAuthReadRepo
)


class SqlAlchemyCreditUoW(CreditUoWPort):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self.credit_read_repo = SqlAlchemyCreditLedgerReadRepo(session)
        self.auth_read_repo = SqlAlchemyAuthReadRepo(session)
