from app.domain.credit.credit_cause import CreditCause
from app.domain.credit.credit_entity import NewCreditEntity
from app.domain.stripe.stripe_exception import (
    AccountIsInvalid,
    BalanceNotExpendedError,
    ChargeNotReadyError,
    IntentIsInvalidError
)
import stripe
from app.domain.payment.payment_entity import NewPaymentEntity
from app.feature.stripe.uow.stripe_uow_port import StripeUoWPort
from app.domain.payment_intent.payment_intent_providers import (
    PaymentProvier
)


class StripeService:
    async def handle_stripe_event(
        self,
        uow: StripeUoWPort,
        event: stripe.Event,
        stripe_client: stripe.StripeClient
    ) -> None:
        match event.type:
            case "payment_intent.succeeded":
                intent = event.data.object
                if not isinstance(intent, stripe.PaymentIntent):
                    raise IntentIsInvalidError()

                provider_payment_id = intent["id"]

                if not await uow.payment_intent_read_repo.intent_exists(
                    provider_payment_id
                ):
                    return

                payment_intent = stripe_client.payment_intents.retrieve(
                    provider_payment_id,
                    params={
                        "expand": ["latest_charge.balance_transaction"]
                    }
                )
                charges = payment_intent.latest_charge
                if charges is None or isinstance(charges, str):
                    raise ChargeNotReadyError()

                balance_tx = charges.balance_transaction
                if balance_tx is None or isinstance(balance_tx, str):
                    raise BalanceNotExpendedError()

                gross_amount = balance_tx.amount
                provider_fee = balance_tx.fee
                net_amount = balance_tx.net

                payment_intent = (
                    await uow.payment_intent_read_repo.get_by_provider_id(
                        provider_payment_id
                    )
                )

                await uow.payment_intent_update_repo.mark_payment_intent(
                    provider_payment_id=provider_payment_id,
                    provider_status=intent["status"]
                )

                payment = NewPaymentEntity(
                    session_id=payment_intent.session_id,
                    user_id=payment_intent.user_id,
                    provider=PaymentProvier.STRIPE.value,
                    provider_payment_id=provider_payment_id,
                    gross_amount_cents=gross_amount,
                    provider_fee_cents=provider_fee,
                    net_amount_cents=net_amount,
                    currency=payment_intent.currency,
                )

                await uow.payment_creation_repo.create_payment(payment)

                print(payment_intent.user_id)
                if payment_intent.credit_applied_cents > 0:
                    credit = NewCreditEntity(
                        user_id=payment_intent.user_id,
                        amount_cents=-payment_intent.credit_applied_cents,
                        currency=payment_intent.currency,
                        cause=CreditCause.SESSION_USAGE
                    )

                    await uow.credit_ledger_creation_repo.append_credit_ledger(
                        credit
                    )

                await uow.session_participation_update_repo.user_paid(
                    payment_intent.session_id,
                    payment_intent.user_id
                )

            case "payment_intent.payment_failed":
                intent = event.data.object
                if not isinstance(intent, stripe.PaymentIntent):
                    raise IntentIsInvalidError()

                provider_payment_id = intent["id"]

                print(provider_payment_id)
                if not await uow.payment_intent_read_repo.intent_exists(
                    provider_payment_id
                ):
                    return

                payment_intent = (
                    await uow.payment_intent_read_repo.get_by_provider_id(
                        provider_payment_id
                    )
                )
                print(intent["status"])
                await uow.payment_intent_update_repo.mark_payment_intent(
                    provider_payment_id=provider_payment_id,
                    provider_status=intent["status"],
                )

                await uow.session_participation_update_repo.cancel_unpaid(
                    payment_intent.session_id,
                    payment_intent.user_id,
                )

            case "payment_intent.canceled":
                intent = event.data.object
                if not isinstance(intent, stripe.PaymentIntent):
                    raise IntentIsInvalidError()

                provider_payment_id = intent["id"]

                if not await uow.payment_intent_read_repo.intent_exists(
                    provider_payment_id
                ):
                    return

                payment_intent = (
                    await uow.payment_intent_read_repo.get_by_provider_id(
                        provider_payment_id
                    )
                )

                await uow.payment_intent_update_repo.mark_payment_intent(
                    provider_payment_id=provider_payment_id,
                    provider_status=intent["status"],
                )

                await uow.session_participation_update_repo.cancel_unpaid(
                    payment_intent.session_id,
                    payment_intent.user_id,
                )
            case "account.updated":
                account = event.data.object
                if not isinstance(account, stripe.Account):
                    raise AccountIsInvalid()

                print(account)

                await (
                    uow.coach_stripe_account_update_repo.update_by_account_id(
                        account_id=account.id,
                        details_submitted=bool(account.details_submitted),
                        charges_enabled=bool(account.charges_enabled),
                        payouts_enabled=bool(account.payouts_enabled)
                    )
                )
            case _:
                return
