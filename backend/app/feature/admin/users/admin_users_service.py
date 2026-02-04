from uuid import UUID
from app.domain.auth.actor_entity import Actor
from app.domain.auth.auth_exceptions import (
    AdminCantSelfRevokeError,
    BaseRoleCannotBeRevokedError
)
from app.domain.auth.permission import Permission
from app.domain.auth.permission_rules import ensure_has_permission
from app.domain.auth.role import Role
from app.feature.admin.users.admin_users_dto import (
    PaginatedUsersDTO,
    RoleDTO,
    UserDTO
)
from app.feature.admin.users.uow.admin_user_uow_port import AdminUserUoWPort
from app.shared.exceptions.commons import NotFoundError


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

    async def get_user(
        self,
        user_id: UUID,
        uow: AdminUserUoWPort,
        actor: Actor,
    ) -> UserDTO:
        ensure_has_permission(actor, Permission.READ_USERS)

        user = await uow.admin_user_read_repository.get_user_by_id(user_id)

        if not user:
            raise NotFoundError()

        return UserDTO(
                id=user.id,
                email=user.email,
                roles=user.roles,
                disabled_at=user.disabled_at,
                created_at=user.created_at
            )

    async def grant_role(
        self,
        user_id: UUID,
        role: RoleDTO,
        uow: AdminUserUoWPort,
        actor: Actor,
    ) -> None:
        ensure_has_permission(actor, Permission.GRANT_ROLE)

        await uow.admin_user_creation_repository.grant_role(
            user_id=user_id,
            role=role.role
        )

    async def revoke_role(
        self,
        user_id: UUID,
        role: RoleDTO,
        uow: AdminUserUoWPort,
        actor: Actor,
    ) -> None:
        ensure_has_permission(actor, Permission.REVOKE_ROLE)

        if role.role == Role.USER:
            raise BaseRoleCannotBeRevokedError()

        if user_id == actor.id and role.role == Role.ADMIN:
            raise AdminCantSelfRevokeError()

        await uow.admin_user_deletion_repository.revoke_role(
            user_id=user_id,
            role=role.role
        )
