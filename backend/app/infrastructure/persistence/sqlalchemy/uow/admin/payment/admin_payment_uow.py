from sqlalchemy.ext.asyncio.session import AsyncSession
from app.feature.admin.payment.uow.admin_payment_uow_port import (
    AdminPaymentUoWPort
)


class SqlAlchemyAdminPaymentUoW(AdminPaymentUoWPort):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session
