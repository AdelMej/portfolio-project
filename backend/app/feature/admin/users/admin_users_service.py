from app.domain.auth.actor_entity import Actor
from app.domain.auth.permission import Permission
from app.domain.auth.permission_rules import ensure_has_permission
from app.feature.admin.users.admin_users_dto import PaginatedUsersDTO, UserDTO
from app.feature.admin.users.uow.admin_user_uow_port import AdminUserUoWPort


class AdminUserService:
    async def get_users(
        self,
        uow: AdminUserUoWPort,
        actor: Actor,
        *,
        limit: int = 50,
        offset: int = 0,
    ) -> PaginatedUsersDTO:
        ensure_has_permission(actor, Permission.READ_USERS)

        users, has_more = await uow.admin_user_read_repository.get_all_users(
            limit=limit,
            offset=offset
        )

        items = [
            UserDTO(
                id=user.id,
                email=user.email,
                roles=user.roles,
                disabled_at=user.disabled_at,
                created_at=user.created_at
            ) for user in users
        ]

        return PaginatedUsersDTO(
            items=items,
            limit=limit,
            offset=offset,
            has_more=has_more,
        )
