from uuid import UUID
from fastapi import APIRouter, Depends
from app.domain.auth.actor_entity import Actor
from app.feature.admin.users.admin_user_dependencies import (
    get_admin_user_service
)
from app.feature.admin.users.admin_users_dto import GetUserDTO
from app.feature.admin.users.admin_users_service import AdminUserService
from app.feature.admin.users.uow.admin_user_read_uow_port import (
    AdminUserReadUoWPort
)
from app.infrastructure.security.provider import get_current_actor

router = APIRouter(
    prefix="/admin/users",
    tags=["admin", "users"]
)


@router.get(
    path="/",
    response_model=list[GetUserDTO]
)
async def admin_get_users(
    uow: AdminUserReadUoWPort,
    actor: Actor = Depends(get_current_actor),
    service: AdminUserService = Depends(get_admin_user_service)
) -> list[GetUserDTO]:
    pass


@router.get(
    path="/{user_id}",
    response_model=list[GetUserDTO]
)
async def admin_get_user_by_id(
    user_id: UUID,
    uow: AdminUserReadUoWPort,
    actor: Actor = Depends(get_current_actor),
    service: AdminUserService = Depends(get_admin_user_service)
) -> list[GetUserDTO]:
    pass
