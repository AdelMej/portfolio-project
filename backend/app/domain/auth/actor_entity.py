from dataclasses import dataclass
from uuid import UUID
from typing import Literal, FrozenSet


@dataclass(frozen=True)
class Actor:
    id: UUID
    type: Literal["user"]          # system comes later
    permissions: FrozenSet[str]
