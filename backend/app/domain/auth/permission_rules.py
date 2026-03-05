from app.domain.auth.actor_entity import Actor
from app.domain.auth.auth_exceptions import PermissionDeniedError
from app.domain.auth.permission import Permission


def ensure_has_permission(
    actor: Actor,
    permission: Permission
) -> None:
    if permission not in actor.permissions:
        raise PermissionDeniedError()
