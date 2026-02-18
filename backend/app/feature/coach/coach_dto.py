from pydantic import BaseModel


class CoachStripeAccountCreationOutputDTO(BaseModel):
    onboarding_url: str | None
