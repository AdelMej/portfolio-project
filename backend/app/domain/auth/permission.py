from enum import Enum

from app.domain.auth.role import Role


class Permission(str, Enum):
    READ_SELF = "user:read:self"
    WRITE_SELF = "user:write:self"
    UPDATE_SELF = "user:update:self"
    DELETE_SELF = "user:delete:self"
    NO_SELF_DELETE = "admin:delete:notSelf"
    ADMIN_READ_USERS = "admin:read:users"
    BAN_USER = "admin:ban:user"
    CREATE_SESSION = "coach:session:create"
    CANCEL_SESSION = "coach:session:cancel"
    ADMIN_CANCEL_SESSION = "admin:session:cancel"
    ADMIN_READ_SESSION = "admin:session:read"
    GRANT_ROLE = "admin:role:grant"
    REVOKE_ROLE = "admin:role:revoke"
    DISABLE_USER = "admin:disable:user"
    REENEABLE_USER = "admin:reenable:user"
    READ_CREDIT = "user:read:credit"
    READ_PAYMENT = "user:read:payment"
    UPDATE_SESSION = "coach:update:session"
    READ_ATTENDANCE = "coach:read:attendance"
    ADMIN_READ_ATTENDANCE = "admin:attendance:read"
    CREATE_ATTENDANCE = "coach:create:attendance"
    SESSION_REGISTRATION = "user:session:registration"
    CANCEL_REGISTRATION = "user:cancel:registration"
    CREATE_STRIPE_ACCOUNT = "coach:create:stripe"
    ADMIN_READ_PAYMENT = "admin:read:payment",
    ADMIN_READ_CREDIT = "admin:read:credit",
    READ_SESSION = "user:read:session"
    COACH_READ_SESSION = "coach:read:session"


ROLE_PERMISSIONS: dict[Role, set[Permission]] = {
    Role.USER: {
        Permission.READ_SELF,
        Permission.WRITE_SELF,
        Permission.UPDATE_SELF,
        Permission.DELETE_SELF,
        Permission.READ_CREDIT,
        Permission.READ_PAYMENT,
        Permission.SESSION_REGISTRATION,
        Permission.CANCEL_REGISTRATION,
        Permission.READ_SESSION
    },
    Role.ADMIN: {
        Permission.READ_SELF,
        Permission.WRITE_SELF,
        Permission.UPDATE_SELF,
        Permission.NO_SELF_DELETE,
        Permission.ADMIN_READ_USERS,
        Permission.ADMIN_READ_SESSION,
        Permission.CREATE_SESSION,
        Permission.ADMIN_CANCEL_SESSION,
        Permission.GRANT_ROLE,
        Permission.REVOKE_ROLE,
        Permission.DISABLE_USER,
        Permission.REENEABLE_USER,
        Permission.ADMIN_READ_ATTENDANCE,
        Permission.ADMIN_READ_PAYMENT,
        Permission.ADMIN_READ_CREDIT
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
        Permission.CREATE_STRIPE_ACCOUNT,
        Permission.COACH_READ_SESSION
    }
}
