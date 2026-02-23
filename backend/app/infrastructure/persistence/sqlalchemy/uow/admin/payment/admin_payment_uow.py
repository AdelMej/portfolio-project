from sqlalchemy.ext.asyncio.session import AsyncSession
from app.feature.admin.payment.uow.admin_payment_uow_port import (
    AdminPaymentUoWPort
)
from app.infrastructure.persistence.sqlalchemy.repositories import (
    SqlAlchemyAdminPaymentReadRepo,
    SqlAlchemyAuthReadRepo
)


class SqlAlchemyAdminPaymentUoW(AdminPaymentUoWPort):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

        self.payment_read_repo = SqlAlchemyAdminPaymentReadRepo(session)
        self.auth_read_repo = SqlAlchemyAuthReadRepo(session)
