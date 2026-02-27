from uuid import UUID
import stripe

from app.domain.auth.actor_entity import Actor
from app.domain.auth.auth_exceptions import AuthUserIsDisabledError
from app.domain.auth.permission import Permission
from app.domain.payment.payment_entity import NewPaymentEntity
from app.domain.payment.payment_exception import PaymentAlreadyPaidError
from app.domain.payment_intent.payment_intent_providers import PaymentProvider
from app.domain.session.session_exception import (
    InvalidCoachAccountError,
    NotOwnerOfSessionError,
    SessionCancelledError,
    SessionNotFinishedError,
    SessionNotFoundError
)
from app.domain.stripe.stripe_exception import (
    AccountIsInvalid,
    CoachPayoutFailedError
)
from app.feature.coach.uow.coach_uow_port import CoachUoWPort
from app.domain.auth.permission_rules import (
    ensure_has_permission
)


class CoachService():
    async def create_onboarding_link(
        self,
        uow: CoachUoWPort,
        actor: Actor,
        client: stripe.StripeClient,
        front_end_url: str
    ) -> str | None:
        ensure_has_permission(actor, Permission.CREATE_STRIPE_ACCOUNT)

        if await uow.auth_read_repo.is_user_disabled(actor.id):
            raise AuthUserIsDisabledError()

        stripe_acount_id = (
            await uow.coach_stripe_account_read_repo.get_account_id(
                actor.id
            )
        )

        if not stripe_acount_id:
            account = await client.accounts.create_async(
                params={
                    "type": "express",
                    "metadata": {
                        "coach_id": str(actor.id)
                    }
                }
            )

            await uow.coach_stripe_account_creation_repo.create_account(
                stripe_acount_id=account.id
            )

            stripe_acount_id = account.id

        link = await client.account_links.create_async(
            params={
                "account": stripe_acount_id,
                "type": "account_onboarding",
                "refresh_url": f"{front_end_url}/stripe/refresh",
                "return_url": f"{front_end_url}/stripe/return",
            }
        )

        return link.url

    async def coach_payout(
        self,
        session_id: UUID,
        uow: CoachUoWPort,
        actor: Actor,
        client: stripe.StripeClient,
    ) -> None:
        if await uow.auth_read_repo.is_user_disabled(actor.id):
            raise AuthUserIsDisabledError()

        if not await uow.coach_stripe_account_read_repo.is_coach_account_valid(
            actor.id
        ):
            raise InvalidCoachAccountError()

        if await uow.payment_read_repo.is_alread_paid(
            session_id=session_id,
            user_id=actor.id
        ):
            raise PaymentAlreadyPaidError()

        if not await uow.session_read_repo.exist_session(
            session_id=session_id
        ):
            raise SessionNotFoundError()

        if not await uow.session_read_repo.is_session_owner(
            session_id=session_id,
            user_id=actor.id
        ):
            raise NotOwnerOfSessionError()

        if await uow.session_read_repo.is_session_cancelled(
            session_id=session_id
        ):
            raise SessionCancelledError()

        if not await uow.session_read_repo.is_session_finished(
            session_id=session_id
        ):
            raise SessionNotFinishedError()

        total, currency = await uow.payment_read_repo.get_payment_for_session(
            session_id=session_id
        )

        if total == 0:
            return

        account_id = await uow.coach_stripe_account_read_repo.get_account_id(
            actor.id
        )

        if not account_id:
            raise AccountIsInvalid()

        try:
            transfer = await client.transfers.create_async(
                params={
                    "amount": total,
                    "currency": currency,
                    "destination": account_id,
                    "metadata": {
                        "session_id": str(session_id),
                        "coach_id": str(actor.id),
                    },
                    "description": f"Coach payout for session {session_id}",
                },
            )
        except stripe.CardError as exc:
            raise CoachPayoutFailedError() from exc
        except stripe.InvalidRequestError as exc:
            raise CoachPayoutFailedError from exc
        except stripe.APIConnectionError as exc:
            raise CoachPayoutFailedError from exc
        except stripe.StripeError as exc:
            raise CoachPayoutFailedError from exc

        payment = NewPaymentEntity(
            session_id=session_id,
            user_id=actor.id,
            provider=PaymentProvider.STRIPE,
            provider_payment_id=transfer.id,
            gross_amount_cents=total,
            provider_fee_cents=0,
            net_amount_cents=total,
            currency=currency
        )

        await uow.payment_creation_repo.create_payment(
            new_payment=payment
        )
