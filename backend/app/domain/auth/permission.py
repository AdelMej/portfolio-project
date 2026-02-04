from enum import Enum

from app.domain.auth.role import Role


class Permission(str, Enum):
    READ_SELF = "read:self"
    WRITE_SELF = "write:self"
    UPDATE_SELF = "update:self"
    DELETE_SELF = "delete:self"
    NO_SELF_DELETE = "delete:nope"
    READ_USERS = "read:users"
    BAN_USER = "ban:user"
    CREATE_SESSION = "session:create"
    CANCEL_SESSION = "session:cancel"

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
        Permission.CREATE_SESSION,
        Permission.CANCEL_SESSION,
    },
    Role.COACH: {
        Permission.READ_SELF,
        Permission.WRITE_SELF,
        Permission.UPDATE_SELF,
        Permission.DELETE_SELF,
        Permission.CREATE_SESSION,
        Permission.CANCEL_SESSION,
    }
}
