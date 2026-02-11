from datetime import datetime
from pydantic import BaseModel, field_validator
from uuid import UUID

from pydantic.fields import Field
from app.shared.rules.currency_rules import (
    CURRENCY_LENGTH
)
from app.shared.rules.session_title_rules import (
    MAX_TITLE_LENGTH,
    MIN_TITLE_LENGTH
)
from app.shared.utils.string_predicate import (
    is_blank,
    is_alpha_ascii
)


class GetOutputDto(BaseModel):
    id: UUID
    coach_id: UUID
    title: str
    starts_at: datetime
    ends_at: datetime
    status: str


class SessionCreationInputDTO(BaseModel):
    title: str = Field(
        ...,
        min_length=MIN_TITLE_LENGTH,
        max_length=MAX_TITLE_LENGTH
    )
    starts_at: datetime
    ends_at: datetime
    price_cents: int
    currency: str = Field(
        ...,
        min_length=CURRENCY_LENGTH,
        max_length=CURRENCY_LENGTH
    )

    @field_validator("price_cents")
    @staticmethod
    def validate_price(price: int) -> int:
        if price < 0:
            raise ValueError("Price cannot be negative")
        return price

    @field_validator("currency")
    @staticmethod
    def validate_currency(currency: str) -> str:
        currency = currency.strip().upper()

        if len(currency) != CURRENCY_LENGTH:
            raise ValueError(
                "currency must be {} character"
                .format(CURRENCY_LENGTH)
            )

        if not is_alpha_ascii(currency):
            raise ValueError("currency must contain only ASCII letters")

        return currency

    @field_validator("title")
    @staticmethod
    def validate_title(title: str) -> str:
        title = title.strip()

        if is_blank(title):
            raise ValueError("title must not be blank")

        if len(title) < MIN_TITLE_LENGTH:
            raise ValueError(
                "title must be at least {} characters long"
                .format(MIN_TITLE_LENGTH)
            )

        if len(title) > MAX_TITLE_LENGTH:
            raise ValueError(
                "title must be less than {} characters long"
                .format(MAX_TITLE_LENGTH)
            )

        return title


class AttendanceOutputDto(BaseModel):
    user_id: UUID


class SessionUpdateInputDTO(BaseModel):
    title: str
    starts_at: datetime
    ends_at: datetime
