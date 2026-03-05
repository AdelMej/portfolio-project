from sqlalchemy.ext.asyncio.session import AsyncSession
from app.feature.admin.credit.uow.admin_credit_uow_port import (
    AdminCreditUoWPort
)
from app.infrastructure.persistence.sqlalchemy.repositories import (
    SqlAlchemyAdminCreditLedgerReadRepo,
    SqlAlchemyAuthReadRepo
)


class SqlAlchemyAdminCreditUoW(AdminCreditUoWPort):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

        self.credit_read_repo = SqlAlchemyAdminCreditLedgerReadRepo(session)
        self.auth_read_repo = SqlAlchemyAuthReadRepo(session)
