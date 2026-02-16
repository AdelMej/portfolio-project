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
        event: stripe.Event
    ) -> None:
        intent = event.data.object
        if not hasattr(intent, "id"):
            return

        provider_payment_id = intent["id"]

        if not await uow.payment_intent_read_repo.intent_exists(
            provider_payment_id
        ):
            return

        print(event.type)
        match event.type:
            case "payment_intent.succeeded":
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
                    amount_cents=payment_intent.amount_cents,
                    currency=payment_intent.currency,
                )

                await uow.payment_creation_repo.create_payment(payment)

                await uow.session_participation_update_repo.user_paid(
                    payment_intent.session_id,
                    payment_intent.user_id
                )

            case "payment_intent.payment_failed":
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

            case "payment_intent.canceled":
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

            case _:
                return
