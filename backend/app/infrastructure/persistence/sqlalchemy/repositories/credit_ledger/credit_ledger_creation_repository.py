from sqlalchemy.exc import DBAPIError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.expression import text
from app.domain.auth.auth_exceptions import PermissionDeniedError
from app.domain.credit.credit_entity import NewCreditEntity
from app.domain.credit.credit_exception import (
    CreditNegativeError,
    InvalidCreditAmount
)
from app.feature.session.repositories import (
    CreditLedgerCreationRepoPort
)
from app.shared.database.sqlstate_extractor import (
    get_sqlstate
)


class SqlAlchemyCreditLedgerCreationRepo(
    CreditLedgerCreationRepoPort
):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create_credit_entry(
        self,
        entry: NewCreditEntity
    ) -> None:
        stmt = text("""
            SELECT
             app_fcn.create_credit_entry(
                :user_id,
                :amount_cents,
                :currency,
                :cause
             )
        """)

        try:
            await self._session.execute(stmt, {
                "user_id": entry.user_id,
                "amount_cents": entry.amount_cents,
                "currency": entry.currency,
                "cause": entry.cause.value
            })
        except DBAPIError as exc:
            code = get_sqlstate(exc)

            if code == "AP401":
                raise PermissionDeniedError() from exc

            if code == "AP400":
                raise InvalidCreditAmount() from exc

            if code == "AB400":
                raise CreditNegativeError() from exc

            raise

    async def append_credit_ledger(
        self,
        credit: NewCreditEntity
    ) -> None:
        stmt = text("""
            SELECT
                app_fcn.append_credit_ledger(
                    :user_id,
                    :amount_cents,
                    :currency,
                    :cause
                )
        """)

        await self._session.execute(stmt, {
            "user_id": credit.user_id,
            "amount_cents": credit.amount_cents,
            "currency": credit.currency,
            "cause": credit.cause.value
        })
