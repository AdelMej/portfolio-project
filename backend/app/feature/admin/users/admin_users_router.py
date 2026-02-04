from uuid import UUID
from fastapi import APIRouter, Depends, Query
from app.domain.auth.actor_entity import Actor
from app.feature.admin.users.admin_user_dependencies import (
    get_admin_user_service
)
from app.feature.admin.users.admin_users_dto import PaginatedUsersDTO, UserDTO
from app.feature.admin.users.admin_users_service import AdminUserService
from app.feature.admin.users.uow.admin_user_uow_port import (
    AdminUserUoWPort
)
from app.infrastructure.security.provider import get_current_actor
from app.infrastructure.persistence.sqlalchemy.provider import (
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
    offset: int = Query(0, ge=1),
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
    pass
