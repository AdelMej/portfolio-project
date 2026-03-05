from fastapi import APIRouter, Depends, HTTPException, Header, Request
import stripe

from app.feature.stripe.stripe_dependencies import get_stripe_service
from app.feature.stripe.stripe_service import StripeService
from app.feature.stripe.uow.stripe_uow_port import StripeUoWPort
from app.infrastructure.persistence.sqlalchemy.provider import get_stripe_uow
from app.infrastructure.settings.provider import (
    get_stripe_client,
    get_web_hook_secret
)

router = APIRouter(
    prefix="/stripe",
    tags=["stripe"]
)


@router.post(
    path="/event",
    status_code=200
)
async def stripe_webhook(
    request: Request,
    uow: StripeUoWPort = Depends(get_stripe_uow),
    stripe_signature: str = Header(None, alias="Stripe-Signature"),
    webhook_secret: str = Depends(get_web_hook_secret),
    stripe_client: stripe.StripeClient = Depends(get_stripe_client),
    service: StripeService = Depends(get_stripe_service)
):
    if not stripe_signature:
        raise HTTPException(status_code=400, detail="Missing Stripe-Signature")

    payload = await request.body()

    try:
        event = stripe.Webhook.construct_event(
            payload=payload,
            sig_header=stripe_signature,
            secret=webhook_secret
        )
    except stripe.SignatureVerificationError:
        raise HTTPException(status_code=400, detail="Invalid signature")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid payload")

    await service.handle_stripe_event(
        uow,
        event,
        stripe_client
    )

    return {"status": "ok"}
