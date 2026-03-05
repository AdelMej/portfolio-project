from pydantic import BaseModel


class GetCreditDTO(BaseModel):
    amount_cents: int
    balance_after_cents: int
    cause: str


class PaginatedCreditOutputDTO(BaseModel):
    items: list[GetCreditDTO]
    limit: int
    offset: int
    has_more: bool
