from datetime import datetime
from uuid import UUID
from app.domain.auth.actor_entity import Actor
from app.domain.auth.auth_exceptions import (
    AuthUserIsDisabledError,
    CoachNotFoundError,
    UserNotFoundError
)
from app.domain.auth.permission import Permission
from app.domain.auth.permission_rules import ensure_has_permission
from app.feature.admin.payment.admin_payment_dto import (
    GetCoachPaymentOutputDTO,
    GetPaymentOutputDTO
)
from app.feature.admin.payment.uow.admin_payment_uow_port import (
    AdminPaymentUoWPort
)


class AdminPaymentService():
    async def get_payments(
        self,
        limit: int,
        offset: int,
        _from: datetime | None,
        to: datetime | None,
        uow: AdminPaymentUoWPort,
        actor: Actor,
    ) -> tuple[list[GetPaymentOutputDTO], bool]:
        ensure_has_permission(actor, Permission.ADMIN_READ_PAYMENT)

        if await uow.auth_read_repo.is_user_disabled(actor.id):
            raise AuthUserIsDisabledError()

        payments, has_more = (
            await uow.payment_read_repo.get_all_payments(
                offset=offset,
                limit=limit,
                _from=_from,
                to=to
            )
        )

        return [
            GetPaymentOutputDTO(
                id=payment.id,
                user_id=payment.user_id,
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

    async def get_user_payments(
        self,
        limit: int,
        offset: int,
        _from: datetime | None,
        to: datetime | None,
        uow: AdminPaymentUoWPort,
        actor: Actor,
        user_id: UUID
    ) -> tuple[list[GetPaymentOutputDTO], bool]:
        ensure_has_permission(actor, Permission.ADMIN_READ_PAYMENT)

        if await uow.auth_read_repo.is_user_disabled(actor.id):
            raise AuthUserIsDisabledError()

        if not await uow.auth_read_repo.exists_user(user_id):
            raise UserNotFoundError()

        payments, has_more = (
            await uow.payment_read_repo.get_user_payments(
                offset=offset,
                limit=limit,
                _from=_from,
                to=to,
                user_id=user_id
            )
        )

        return [
            GetPaymentOutputDTO(
                id=payment.id,
                user_id=payment.user_id,
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

    async def get_coach_payments(
        self,
        limit: int,
        offset: int,
        _from: datetime | None,
        to: datetime | None,
        uow: AdminPaymentUoWPort,
        actor: Actor,
        coach_id: UUID
    ) -> tuple[list[GetCoachPaymentOutputDTO], bool]:
        ensure_has_permission(actor, Permission.ADMIN_READ_PAYMENT)

        if await uow.auth_read_repo.is_user_disabled(actor.id):
            raise AuthUserIsDisabledError()

        if not await uow.auth_read_repo.exists_coach(coach_id):
            raise CoachNotFoundError()

        payments, has_more = (
            await uow.payment_read_repo.get_coach_payments(
                offset=offset,
                limit=limit,
                _from=_from,
                to=to,
                coach_id=coach_id
            )
        )

        return [
            GetCoachPaymentOutputDTO(
                id=payment.id,
                coach_id=payment.user_id,
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
