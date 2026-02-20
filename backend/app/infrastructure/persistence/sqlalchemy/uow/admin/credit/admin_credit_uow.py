from sqlalchemy.ext.asyncio.session import AsyncSession
from app.feature.admin.credit.uow.admin_credit_uow_port import (
    AdminCreditUoWPort
)


class SqlAlchemyAdminCreditUoW(AdminCreditUoWPort):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session
