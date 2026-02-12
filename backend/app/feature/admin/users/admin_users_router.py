from uuid import UUID
from fastapi import APIRouter, Depends, Query
from app.domain.auth.actor_entity import Actor
from app.feature.admin.users.admin_user_dependencies import (
    get_admin_user_service
)
from app.feature.admin.users.admin_users_dto import (
    PaginatedUsersDTO,
    UserDTO,
    RoleDTO
)
from app.feature.admin.users.admin_users_service import AdminUserService
from app.feature.admin.users.uow.admin_user_system_uow_port import (
    AdminUserSystemUoWPort
)
from app.feature.admin.users.uow.admin_user_uow_port import (
    AdminUserUoWPort
)
from app.infrastructure.security.provider import get_current_actor
from app.infrastructure.persistence.sqlalchemy.provider import (
    get_admin_system_user_uow,
    get_admin_user_uow
)


router = APIRouter(
    prefix="/admin/users",
    tags=["admin"]
)


@router.get(
    path="/",
    response_model=PaginatedUsersDTO
)
async def admin_get_users(
    uow: AdminUserUoWPort = Depends(get_admin_user_uow),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    actor: Actor = Depends(get_current_actor),
    service: AdminUserService = Depends(get_admin_user_service)
) -> PaginatedUsersDTO:

    return await service.get_users(
        uow=uow,
        actor=actor,
        limit=limit,
        offset=offset
    )


@router.get(
    path="/{user_id}",
    response_model=UserDTO
)
async def admin_get_user_by_id(
    user_id: UUID,
    uow: AdminUserUoWPort = Depends(get_admin_user_uow),
    actor: Actor = Depends(get_current_actor),
    service: AdminUserService = Depends(get_admin_user_service)
) -> UserDTO:

    return await service.get_user(
        user_id=user_id,
        uow=uow,
        actor=actor,
    )


@router.post(
    path="/{user_id}/grant-role",
    status_code=204
)
async def admin_grant_role(
    user_id: UUID,
    role: RoleDTO,
    uow: AdminUserSystemUoWPort = Depends(get_admin_system_user_uow),
    actor: Actor = Depends(get_current_actor),
    service: AdminUserService = Depends(get_admin_user_service)
) -> None:

    await service.grant_role(
        user_id=user_id,
        role=role,
        uow=uow,
        actor=actor
    )


@router.post(
    path="/{user_id}/revoke-role",
    status_code=204
)
async def admin_revoke_role(
    user_id: UUID,
    role: RoleDTO,
    uow: AdminUserSystemUoWPort = Depends(get_admin_system_user_uow),
    actor: Actor = Depends(get_current_actor),
    service: AdminUserService = Depends(get_admin_user_service)
) -> None:

    await service.revoke_role(
        user_id=user_id,
        role=role,
        uow=uow,
        actor=actor
    )


@router.post(
    path="/{user_id}/disable",
    status_code=204
)
async def admin_disable_user(
    user_id: UUID,
    uow: AdminUserSystemUoWPort = Depends(get_admin_system_user_uow),
    actor: Actor = Depends(get_current_actor),
    service: AdminUserService = Depends(get_admin_user_service)
) -> None:

    await service.disable_user(
        user_id=user_id,
        uow=uow,
        actor=actor
    )


@router.post(
    path="/{user_id}/reenable",
    status_code=204
)
async def admin_reenable_user(
    user_id: UUID,
    uow: AdminUserSystemUoWPort = Depends(get_admin_system_user_uow),
    actor: Actor = Depends(get_current_actor),
    service: AdminUserService = Depends(get_admin_user_service)
) -> None:

    await service.reenable_user(
        user_id=user_id,
        uow=uow,
        actor=actor
    )
