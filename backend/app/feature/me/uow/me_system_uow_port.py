from typing import Protocol

from app.feature.me.repositories import (
    AuthReadRepoPort,
    AuthUpdateRepoPort,
    MeDeleteRepoPort,
    MeUpdateRepoPort,
    SessionParticipationReadRepoPort,
    SessionReadRepoPort
)


class MeSystemUoWPort(Protocol):
    me_update_repo: MeUpdateRepoPort
    me_delete_repo: MeDeleteRepoPort
    auth_read_repo: AuthReadRepoPort
    auth_update_repo: AuthUpdateRepoPort
    session_participation_read_repo: SessionParticipationReadRepoPort
    session_read_repo: SessionReadRepoPort
