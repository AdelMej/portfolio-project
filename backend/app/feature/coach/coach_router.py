from uuid import UUID
from fastapi import APIRouter, Depends
import stripe

from app.feature.coach.coach_dependencies import get_coach_service
from app.feature.coach.coach_dto import CoachStripeAccountCreationOutputDTO
from app.feature.coach.coach_service import CoachService
from app.feature.coach.uow.coach_uow_port import CoachUoWPort
from app.domain.auth.actor_entity import Actor
from app.infrastructure.security.provider import get_current_actor
from app.infrastructure.settings.provider import (
    get_front_end_link,
    get_stripe_client
)
from app.infrastructure.persistence.sqlalchemy.provider import get_coach_uow

router = APIRouter(
    prefix="/coach",
    tags=["coach"]
)


@router.post('/stripe/account')
async def coach_account(
    uow: CoachUoWPort = Depends(get_coach_uow),
    actor: Actor = Depends(get_current_actor),
    client: stripe.StripeClient = Depends(get_stripe_client),
    service: CoachService = Depends(get_coach_service),
    front_end_url: str = Depends(get_front_end_link)
) -> CoachStripeAccountCreationOutputDTO:
    link = await service.create_onboarding_link(
        uow=uow,
        actor=actor,
        client=client,
        front_end_url=front_end_url
    )

    return CoachStripeAccountCreationOutputDTO(
        onboarding_url=link
    )


@router.post(
    path='/{session_id}/payout',
    status_code=204
)
async def coach_payout(
    session_id: UUID,
    uow: CoachUoWPort = Depends(get_coach_uow),
    actor: Actor = Depends(get_current_actor),
    client: stripe.StripeClient = Depends(get_stripe_client),
    service: CoachService = Depends(get_coach_service)
) -> None:
    await service.coach_payout(
        session_id=session_id,
        uow=uow,
        actor=actor,
        client=client,
    )
