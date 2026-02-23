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
from app.shared.rules.user_profile_rules import (
    MAX_FIRST_NAME_LENGTH,
    MAX_LAST_NAME_LENGTH,
    MIN_FIRST_NAME_LENGTH,
    MIN_LAST_NAME_LENGTH
)
from app.shared.utils.string_predicate import (
    is_blank,
    is_alpha_ascii
)


class CoachPublicDto(BaseModel):
    id: UUID
    first_name: str
    last_name: str


class GetOutputDto(BaseModel):
    id: UUID
    coach: CoachPublicDto
    title: str
    starts_at: datetime
    ends_at: datetime
    price_cents: int
    currency: str
    status: str


class PaginatedSessionsOutputDTO(BaseModel):
    items: list[GetOutputDto]
    limit: int
    offset: int
    has_more: bool


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
    first_name: str = Field(
        ...,
        min_length=MIN_FIRST_NAME_LENGTH,
        max_length=MAX_FIRST_NAME_LENGTH
    )
    last_name: str = Field(
        ...,
        min_length=MIN_LAST_NAME_LENGTH,
        max_length=MAX_LAST_NAME_LENGTH
    )


class SessionUpdateInputDTO(BaseModel):
    title: str = Field(
        ...,
        min_length=MIN_TITLE_LENGTH,
        max_length=MAX_TITLE_LENGTH
    )
    starts_at: datetime
    ends_at: datetime

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


class AttendanceLineInputDTO(BaseModel):
    user_id: UUID = Field(...)
    attended: bool = Field(...)

    model_config = {
        "extra": "forbid"
    }


class AttendanceInputDTO(BaseModel):
    attendance: list[AttendanceLineInputDTO] = Field(
        ...,
        min_length=1
    )

    model_config = {
        "extra": "forbid"
    }

    @field_validator("attendance")
    @classmethod
    def no_duplicate_users(
        cls,
        attendance: list[AttendanceLineInputDTO]
    ) -> list[AttendanceLineInputDTO]:

        seen = set()

        for line in attendance:
            if line.user_id in seen:
                raise ValueError(
                    f"duplicate user_id in attendance list: {line.user_id}"
                )
            seen.add(line.user_id)

        return attendance


class RegistrationOutputDTO(BaseModel):
    require_payment: bool
    payment_intent_client_secret: str | None
