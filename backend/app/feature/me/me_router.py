from datetime import datetime
from fastapi import APIRouter, Depends, Query
from fastapi.responses import Response

from app.domain.auth.actor_entity import Actor
from app.feature.auth.auth_dto import GetMeOutputDTO
from app.feature.me.me_dependencies import get_me_service
from app.feature.me.me_dto import (
GetMeProfileOutputDTO,
MeEmailChangeInputDTO,
MePasswordChangeInputDTO,
PaginatedSessionsOutputDTO,
UpdateMeProfileInputDTO
)
from app.feature.me.me_service import MeService
from app.feature.me.uow.me_system_uow_port import MeSystemUoWPort
from app.feature.me.uow.me_uow_port import MeUoWPort
from app.infrastructure.persistence.sqlalchemy.provider import (
get_me_system_uow,
get_me_uow
)
from app.infrastructure.security.provider import (
    get_current_actor,
    get_password_hasher
)
from app.shared.security.password_hasher_port import PasswordHasherPort


router = APIRouter(
    prefix="/me",
    tags=["me"]
)


@router.get(
    "/",
    response_model=GetMeOutputDTO,
    status_code=200
)
async def get_me(
    uow: MeUoWPort = Depends(get_me_uow),
    actor: Actor = Depends(get_current_actor),
    service: MeService = Depends(get_me_service)
) -> GetMeOutputDTO:
    user = await service.get_me(actor, uow)

    return GetMeOutputDTO(
        email=user.email,
        roles=user.roles
    )


@router.patch(
    "/email-change",
    status_code=204
)
async def email_change_me(
    input: MeEmailChangeInputDTO,
    uow: MeSystemUoWPort = Depends(get_me_system_uow),
    actor: Actor = Depends(get_current_actor),
    service: MeService = Depends(get_me_service)
) -> None:
    await service.email_change_me(actor, uow, input)


@router.patch(
    "/password-change",
    status_code=204
)
async def password_change_me(
    input: MePasswordChangeInputDTO,
    password_hasher: PasswordHasherPort = Depends(get_password_hasher),
    uow: MeSystemUoWPort = Depends(get_me_system_uow),
    actor: Actor = Depends(get_current_actor),
    service: MeService = Depends(get_me_service)
) -> None:

    await service.password_change_me(
        input=input,
        password_hasher=password_hasher,
        actor=actor,
        uow=uow,
    )


@router.get(
    "/profile",
    status_code=200,
    response_model=GetMeProfileOutputDTO
)
async def get_me_profile(
    actor: Actor = Depends(get_current_actor),
    uow: MeUoWPort = Depends(get_me_uow),
    service: MeService = Depends(get_me_service)
) -> GetMeProfileOutputDTO:

    return await service.get_me_profile(
        actor=actor,
        uow=uow
    )


@router.put(
    "/profile",
    status_code=204
)
async def update_me_profile(
    input: UpdateMeProfileInputDTO,
    actor: Actor = Depends(get_current_actor),
    uow: MeUoWPort = Depends(get_me_uow),
    service: MeService = Depends(get_me_service)
) -> None:

    await service.update_me_profile(
        input=input,
        actor=actor,
        uow=uow
    )


@router.delete(
    "/",
    status_code=204
)
async def delete_me(
    response: Response,
    actor: Actor = Depends(get_current_actor),
    uow: MeSystemUoWPort = Depends(get_me_system_uow),
    service: MeService = Depends(get_me_service),
) -> None:

    await service.delete_me(
        actor=actor,
        uow=uow,
    )

    response.delete_cookie(
        key="refresh_token",
        path="/auth"
    )


@router.get(
    path="/sessions/"
)
async def get_own_sessions(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    _from: datetime | None = Query(None),
    to: datetime | None = Query(None),
    actor: Actor = Depends(get_current_actor),
    uow: MeUoWPort = Depends(get_me_uow),
    service: MeService = Depends(get_me_service)
) -> PaginatedSessionsOutputDTO:
    items, has_more = await service.get_own_sessions(
        offset=offset,
        limit=limit,
        _from=_from,
        to=to,
        uow=uow,
        actor=actor
    )

    return PaginatedSessionsOutputDTO(
        items=items,
        limit=limit,
        offset=offset,
        has_more=has_more
    )
