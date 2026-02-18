import stripe

from app.domain.auth.actor_entity import Actor
from app.domain.auth.permission import Permission
from app.feature.coach.uow.coach_uow_port import CoachUoWPort
from app.domain.auth.permission_rules import (
    ensure_has_permission
)


class CoachService():
    async def create_onboarding_link(
        self,
        uow: CoachUoWPort,
        actor: Actor,
        client: stripe.StripeClient
    ) -> str | None:
        ensure_has_permission(actor, Permission.CREATE_STRIPE_ACCOUNT)

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
                "refresh_url": "https://your-app/stripe/refresh",
                "return_url": "https://your-app/stripe/return",
            }
        )

        return link.url
