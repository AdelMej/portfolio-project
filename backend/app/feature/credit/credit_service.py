from datetime import datetime
from app.domain.auth.actor_entity import Actor
from app.domain.auth.permission import Permission
from app.domain.auth.permission_rules import ensure_has_permission
from app.feature.credit.credit_dto import GetCreditDTO
from app.feature.credit.uow.credit_uow_port import CreditUoWPort


class CreditService():
    async def get_all_credits(
        self,
        limit: int,
        offset: int,
        _from: datetime | None,
        to: datetime | None,
        uow: CreditUoWPort,
        actor: Actor,
    ) -> tuple[list[GetCreditDTO], bool]:
        ensure_has_permission(actor, Permission.READ_CREDIT)

        credits, has_more = (
            await uow.credit_read_repo.get_credit_by_user_id(
                limit=limit,
                offset=offset,
                to=to,
                _from=_from,
                user_id=actor.id
            )
        )

        return [
            GetCreditDTO(
                amount_cents=credit.amount_cents,
                balance_after_cents=credit.balance_after_cents,
                cause=credit.cause,
            ) for credit in credits
        ], has_more
