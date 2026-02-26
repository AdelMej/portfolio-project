from typing import Protocol
from app.feature.me.repositories import (
    AuthReadRepoPort,
    MeReadRepoPort,
    MeUpdateRepoPort,
    SessionParticipationReadRepoPort,
    SessionReadRepoPort
)


class MeUoWPort(Protocol):
    me_read_repo: MeReadRepoPort
    me_update_repo: MeUpdateRepoPort
    auth_read_repo: AuthReadRepoPort
    session_participation_read_repo: SessionParticipationReadRepoPort
    session_read_repo: SessionReadRepoPort
