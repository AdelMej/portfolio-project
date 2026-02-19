from enum import Enum

from app.domain.auth.role import Role


class Permission(str, Enum):
    READ_SELF = "read:self"
    WRITE_SELF = "write:self"
    UPDATE_SELF = "update:self"
    DELETE_SELF = "delete:self"
    NO_SELF_DELETE = "delete:notSelf"
    READ_USERS = "read:users"
    BAN_USER = "ban:user"
    CREATE_SESSION = "session:create"
    CANCEL_SESSION = "session:cancel"
    GRANT_ROLE = "role:grant"
    REVOKE_ROLE = "role:revoke"
    DISABLE_USER = "disable:user"
    REENEABLE_USER = "reenable:user"
    READ_CREDIT = "read:credit"
    READ_PAYMENT = "read:payment"
    UPDATE_SESSION = "update:session"
    READ_ATTENDANCE = "read:attendance"
    CREATE_ATTENDANCE = "create:attendance"
    SESSION_REGISTRATION = "session:registration"
    CANCEL_REGISTRATION = "cancel:registration"
    CREATE_STRIPE_ACCOUNT = "creat:stripe"


ROLE_PERMISSIONS: dict[Role, set[Permission]] = {
    Role.USER: {
        Permission.READ_SELF,
        Permission.WRITE_SELF,
        Permission.UPDATE_SELF,
        Permission.DELETE_SELF,
        Permission.READ_CREDIT,
        Permission.READ_PAYMENT,
        Permission.SESSION_REGISTRATION,
        Permission.CANCEL_REGISTRATION
    },
    Role.ADMIN: {
        Permission.READ_SELF,
        Permission.WRITE_SELF,
        Permission.UPDATE_SELF,
        Permission.NO_SELF_DELETE,
        Permission.READ_USERS,
        Permission.CREATE_SESSION,
        Permission.CANCEL_SESSION,
        Permission.GRANT_ROLE,
        Permission.REVOKE_ROLE,
        Permission.DISABLE_USER,
        Permission.REENEABLE_USER,
        Permission.READ_CREDIT,
        Permission.READ_PAYMENT
    },
    Role.COACH: {
        Permission.READ_SELF,
        Permission.WRITE_SELF,
        Permission.UPDATE_SELF,
        Permission.DELETE_SELF,
        Permission.CREATE_SESSION,
        Permission.CANCEL_SESSION,
        Permission.UPDATE_SESSION,
        Permission.READ_ATTENDANCE,
        Permission.CREATE_ATTENDANCE,
        Permission.CREATE_STRIPE_ACCOUNT
    }
}
