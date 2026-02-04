from enum import Enum

from app.domain.auth.role import Role


class Permission(str, Enum):
    READ_SELF = "read:self"
    WRITE_SELF = "write:self"
    UPDATE_SELF = "update:self"
    DELETE_SELF = "delete:self"
    NO_SELF_DELETE = "delete:notSelf"
    READ_USERS = "read:users"
    GRANT_ROLE = "role:grant"
    REVOKE_ROLE = "role:revoke"
    BAN_USER = "ban:user"


ROLE_PERMISSIONS: dict[Role, set[Permission]] = {
    Role.USER: {
        Permission.READ_SELF,
        Permission.WRITE_SELF,
        Permission.UPDATE_SELF,
        Permission.DELETE_SELF
    },
    Role.ADMIN: {
        Permission.READ_SELF,
        Permission.WRITE_SELF,
        Permission.UPDATE_SELF,
        Permission.NO_SELF_DELETE,
        Permission.READ_USERS,
        Permission.BAN_USER,
        Permission.GRANT_ROLE,
        Permission.REVOKE_ROLE
    },
    Role.COACH: {
        Permission.READ_SELF,
        Permission.WRITE_SELF,
        Permission.UPDATE_SELF,
        Permission.DELETE_SELF
    }
}
