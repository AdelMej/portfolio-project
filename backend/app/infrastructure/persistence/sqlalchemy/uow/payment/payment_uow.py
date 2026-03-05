from sqlalchemy.ext.asyncio import AsyncSession
from app.feature.payment.uow.payment_uow_port import (
    PaymentUoWPort
)
from app.infrastructure.persistence.sqlalchemy.repositories import (
    SqlAlchemyPaymentReadRepo,
    SqlAlchemyAuthReadRepo
)


class SqlAlchemyPaymenUoW(PaymentUoWPort):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

        self.payment_read_repo = SqlAlchemyPaymentReadRepo(session)
        self.auth_read_repo = SqlAlchemyAuthReadRepo(session)
