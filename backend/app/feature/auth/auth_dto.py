from pydantic import BaseModel, EmailStr, Field, field_validator
from app.domain.auth.role import Role
from app.shared.rules.email_rules import (
    MIN_EMAIL_LENGTH,
    MAX_EMAIL_LENGTH,
)
from app.shared.rules.password_rules import (
    MIN_PASSWORD_LENGTH,
    MAX_PASSWORD_LENGTH
)
from app.shared.rules.user_profile_rules import (
    MIN_FIRST_NAME_LENGTH,
    MAX_FIRST_NAME_LENGTH,
    MIN_LAST_NAME_LENGTH,
    MAX_LAST_NAME_LENGTH
)
from app.shared.utils.string_predicate import (
    contains_digit,
    contains_lowercase,
    contains_special,
    contains_uppercase,
    is_blank
)


class LoginInputDTO(BaseModel):
    email: EmailStr = Field(
        ...,
        min_length=MIN_EMAIL_LENGTH,
        max_length=MAX_EMAIL_LENGTH
    )
    password: str = Field(
        ...,
        min_length=MIN_PASSWORD_LENGTH,
        max_length=MAX_PASSWORD_LENGTH
    )


class TokenOutputDTO(BaseModel):
    access_token: str
    token_type: str


class GetMeOutputDTO(BaseModel):
    email: EmailStr = Field(
        ...,
        min_length=MIN_EMAIL_LENGTH,
        max_length=MAX_EMAIL_LENGTH
    )
    roles: set[Role]


class MeEmailChangeInputDTO(BaseModel):
    email: EmailStr = Field(
        ...,
        min_length=MIN_EMAIL_LENGTH,
        max_length=MAX_EMAIL_LENGTH
    )


class MePasswordChangeInputDTO(BaseModel):
    old_password: str
    new_password: str = Field(
        ...,
        min_length=MIN_PASSWORD_LENGTH,
        max_length=MAX_PASSWORD_LENGTH
    )

    @field_validator("new_password")
    @classmethod
    def password_policy(cls, password: str) -> str:
        password = password.strip()

        if is_blank(password):
            raise ValueError("password must not be blank")

        if len(password) < MIN_PASSWORD_LENGTH:
            raise ValueError(
                "password must be at least {} characters long"
                .format(MIN_PASSWORD_LENGTH)
            )

        if len(password) > MAX_PASSWORD_LENGTH:
            raise ValueError(
                "password must be less than {} characters"
                .format(MAX_PASSWORD_LENGTH)
            )

        if not contains_digit(password):
            raise ValueError("password must contain a digit")

        if not contains_lowercase(password):
            raise ValueError("password must contain a lowercase character")

        if not contains_uppercase(password):
            raise ValueError("password must contain an uppercase character")

        if not contains_special(password):
            raise ValueError("password must contain a special character")

        return password


class RegistrationInputDTO(BaseModel):
    email: EmailStr = Field(
        ...,
        min_length=MIN_EMAIL_LENGTH,
        max_length=MAX_EMAIL_LENGTH
    )
    password: str = Field(
        ...,
        min_length=MIN_PASSWORD_LENGTH,
        max_length=MAX_PASSWORD_LENGTH
    )
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

    @field_validator("password")
    @classmethod
    def password_policy(cls, password: str) -> str:
        password = password.strip()

        if is_blank(password):
            raise ValueError("password must not be blank")

        if len(password) < MIN_PASSWORD_LENGTH:
            raise ValueError(
                "password must be at least {} characters long"
                .format(MIN_PASSWORD_LENGTH)
            )

        if len(password) > MAX_PASSWORD_LENGTH:
            raise ValueError(
                "password must be less than {} characters"
                .format(MAX_PASSWORD_LENGTH)
            )

        if not contains_digit(password):
            raise ValueError("password must contain a digit")

        if not contains_lowercase(password):
            raise ValueError("password must contain a lowercase character")

        if not contains_uppercase(password):
            raise ValueError("password must contain an uppercase character")

        if not contains_special(password):
            raise ValueError("password must contain a special character")

        return password

    @field_validator("first_name")
    @classmethod
    def first_name_policy(cls, first_name: str) -> str:
        first_name = first_name.strip()

        if is_blank(first_name):
            raise ValueError("first name must not be blank")

        if len(first_name) < MIN_FIRST_NAME_LENGTH:
            raise ValueError(
                "first name must be at least {} character long"
                .format(MIN_FIRST_NAME_LENGTH)
            )

        if len(first_name) > MAX_FIRST_NAME_LENGTH:
            raise ValueError(
                "first name must be less than {} characters"
                .format(MAX_FIRST_NAME_LENGTH)
            )

        return first_name

    @field_validator("last_name")
    @classmethod
    def last_name_policu(cls, last_name: str) -> str:
        last_name.strip()

        if is_blank(last_name):
            raise ValueError("last name must not be blank")

        if len(last_name) < MIN_LAST_NAME_LENGTH:
            raise ValueError(
                "last name must be at least {} character long"
                .format(MIN_LAST_NAME_LENGTH)
            )

        if len(last_name) > MAX_LAST_NAME_LENGTH:
            raise ValueError(
                "last name must be less than {} characters"
                .format(MAX_LAST_NAME_LENGTH)
            )

        return last_name
