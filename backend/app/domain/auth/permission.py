from enum import Enum

from app.domain.auth.role import Role


class Permission(str, Enum):
    READ_SELF = "read:self"
    WRITE_SELF = "write:self"
    UPDATE_SELF = "update:self"
    DELETE_SELF = "delete:self"
    NO_SELF_DELETE = "delete:notSelf"
    ADMIN_READ_USERS = "admin:read:users"
    BAN_USER = "ban:user"
    CREATE_SESSION = "session:create"
    CANCEL_SESSION = "session:cancel"
    ADMIN_CANCEL_SESSION = "admin:session:cancel"
    ADMIN_READ_SESSION = "admin:session:read"
    GRANT_ROLE = "role:grant"
    REVOKE_ROLE = "role:revoke"
    DISABLE_USER = "disable:user"
    REENEABLE_USER = "reenable:user"
    READ_CREDIT = "read:credit"
    READ_PAYMENT = "read:payment"
    UPDATE_SESSION = "update:session"
    READ_ATTENDANCE = "read:attendance"
    ADMIN_READ_ATTENDANCE = "admin:attendance:read"
    CREATE_ATTENDANCE = "create:attendance"
    SESSION_REGISTRATION = "session:registration"
    CANCEL_REGISTRATION = "cancel:registration"
    CREATE_STRIPE_ACCOUNT = "create:stripe"
    COACH_PAYOUT = "coach:payout",
    ADMIN_READ_PAYMENT = "admin:read:payment",
    ADMIN_READ_CREDIT = "admin:read:credit"


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
        Permission.COACH_PAYOUT
    }
}
