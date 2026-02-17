from datetime import datetime
from app.domain.auth.actor_entity import Actor
from app.domain.auth.permission import Permission
from app.feature.payment.payment_dto import GetPaymentOutputDTO
from app.feature.payment.uow.payment_uow_port import PaymentUoWPort
from app.domain.auth.permission_rules import ensure_has_permission


class PaymentService():
    async def get_payments(
        self,
        limit: int,
        offset: int,
        _from: datetime | None,
        to: datetime | None,
        uow: PaymentUoWPort,
        actor: Actor,
    ) -> tuple[list[GetPaymentOutputDTO], bool]:
        ensure_has_permission(actor, Permission.READ_PAYMENT)
        payments, has_more = (
            await uow.payment_read_repo.get_payment_by_user_id(
                offset=offset,
                limit=limit,
                _from=_from,
                to=to,
                user_id=actor.id
            )
        )

        return [
            GetPaymentOutputDTO(
                session_id=payment.session_id,
                provider=payment.provider,
                provider_payment_id=payment.provider_payment_id,
                gross_amount_cents=payment.gross_amount_cents,
                provider_fee_cents=payment.provider_fee_cents,
                net_amount_cents=payment.net_amount_cents,
                currency=payment.currency,
                created_at=payment.created_at
            ) for payment in payments
        ], has_more
