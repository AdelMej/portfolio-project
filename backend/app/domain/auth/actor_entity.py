from collections.abc import Iterable
from dataclasses import dataclass
from uuid import UUID
from typing import Literal, FrozenSet
from app.domain.auth.role import Role


@dataclass(frozen=True)
class Actor:
    id: UUID
    type: Literal["user"]          # system comes later
    permissions: FrozenSet[str]


@dataclass(frozen=True)
class TokenActor:
    id: UUID
    roles: Iterable[Role]
