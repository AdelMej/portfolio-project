from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import logging

from app.feature.auth.auth_exception import (
    InvalidTokenError,
    InvalidCredentialsError,
    RegistrationFailed
)
from app.domain.auth.auth_exceptions import (
    PermissionDeniedError,
    PasswordIsBlankError,
    PasswordMissingDigitError,
    PasswordMissingUppercaseError,
    PasswordMissingSpecialCharError,
    PasswordMissingLowercaseError,
    PasswordTooWeakError,
    PasswordTooLongError,
    PasswordMissmatchError,
    PasswordTooShortError,
    PasswordReuseError,
    EmailSpaceError,
    EmailIsBlankError,
    EmailTooShortError,
    EmailTooLongError,
    EmailInvalidDomainError,
    EmailLocalPartTooLongError,
    EmailInvalidLocalPartError,
    EmailInvalidAtCountError,
    EmailAlreadyExistError,
    RefreshTokenIsBlankError,
    RefreshTokenTooShortError,
    RevokedRefreshTokenError,
    InvalidRefreshTokenError,
    ExpiredRefreshTokenError,
    RefreshTokenTooLongError,
    AdminCantSelfDeleteError,
    RefreshTokenNotFoundError,
    UserDisabledError,
    AdminCantSelfRevokeError,
    BaseRoleCannotBeRevokedError,
    AdminCantSelfDisableError,
    AdminCantSelfRennableError,
    AuthUserIsDisabledError
)
from app.shared.rules.password_rules import (
    MIN_PASSWORD_LENGTH,
    MAX_PASSWORD_LENGTH,
)
from app.shared.rules.email_rules import (
    MIN_EMAIL_LENGTH,
    MAX_EMAIL_LENGTH,
    MAX_LOCAL_PART
)
from app.shared.rules.refresh_token_rules import (
    REFRESH_TOKEN_MIN_SIZE,
    REFRESH_TOKEN_MAX_SIZE
)
logger = logging.getLogger("app.exceptions")


def register_exception_handler(app: FastAPI):

    @app.exception_handler(UserDisabledError)
    async def user_disabled(
        request: Request,
        exc: AdminCantSelfDeleteError
    ) -> JSONResponse:
        logger.info(
            "user is disabled",
            extra={
                "error": exc.__class__.__name__,
                "path": str(request.url.path),
                "client": request.client.host if request.client else None,
            }
        )

        return JSONResponse(
            content={
                "error": "User disabled"
            },
            status_code=401
        )

    @app.exception_handler(PermissionDeniedError)
    async def permission_denied(
        request: Request,
        exc: PermissionDeniedError
    ) -> JSONResponse:
        logger.info(
            "Permission denied",
            extra={
                "error": exc.__class__.__name__,
                "path": str(request.url.path),
                "client": request.client.host if request.client else None,
            }
        )

        return JSONResponse(
            content={"error": "Permission denied"},
            status_code=403
        )

    @app.exception_handler(InvalidTokenError)
    async def invalid_refresh_token(
        request: Request,
        exc: InvalidTokenError
    ) -> JSONResponse:
        logger.info(
            "Invalid token",
            extra={
                "error": exc.__class__.__name__,
                "path": str(request.url.path),
                "client": request.client.host if request.client else None,
            }
        )

        return JSONResponse(
            content={"error": "Invalid token"},
            status_code=401
        )

    @app.exception_handler(InvalidCredentialsError)
    async def invalid_credentials(
        request: Request,
        exc: InvalidCredentialsError
    ) -> JSONResponse:
        logger.info(
            "Invalid credentials",
            extra={
                "error": exc.__class__.__name__,
                "path": str(request.url.path),
                "client": request.client.host if request.client else None,
            }
        )

        return JSONResponse(
            content={"error": "Invalid credentials"},
            status_code=401
        )

    @app.exception_handler(RegistrationFailed)
    async def registration_failed(
        request: Request,
        exc: RegistrationFailed
    ) -> JSONResponse:
        logger.info(
            "regsitration failure",
            extra={
                "error": exc.__class__.__name__,
                "path": str(request.url.path),
                "client": request.client.host if request.client else None,
            }
        )

        return JSONResponse(
            content={"error": "Registration Failed"},
            status_code=400
        )
    # ---------------------------
    # --- Password Exceptions ---
    # ---------------------------

    @app.exception_handler(PasswordIsBlankError)
    async def password_is_blank(
        request: Request,
        exc: PasswordIsBlankError
    ) -> JSONResponse:
        logger.info(
            "Password is blank",
            extra={
                "error": exc.__class__.__name__,
                "path": str(request.url.path),
                "client": request.client.host if request.client else None,
            }
        )

        return JSONResponse(
            content={"error": "password cannot be blank"},
            status_code=400
        )

    @app.exception_handler(PasswordTooShortError)
    async def password_too_short(
        request: Request,
        exc: PasswordTooShortError
    ) -> JSONResponse:
        logger.info(
            "Password is too short",
            extra={
                "error": exc.__class__.__name__,
                "path": str(request.url.path),
                "client": request.client.host if request.client else None,
            }
        )

        return JSONResponse(
            content={
                "error": "password must be at least {} character long"
                .format(MIN_PASSWORD_LENGTH)
            },
            status_code=400
        )

    @app.exception_handler(PasswordTooLongError)
    async def password_too_long(
        request: Request,
        exc: PasswordTooLongError
    ) -> JSONResponse:
        logger.info(
            "Password is too long",
            extra={
                "error": exc.__class__.__name__,
                "path": str(request.url.path),
                "client": request.client.host if request.client else None,
            }
        )

        return JSONResponse(
            content={
                "error": "password must be less than {} character long"
                .format(MAX_PASSWORD_LENGTH)
            },
            status_code=400
        )

    @app.exception_handler(PasswordMissingLowercaseError)
    async def password_missing_lowercase(
        request: Request,
        exc: PasswordMissingLowercaseError
    ) -> JSONResponse:
        logger.info(
            "Password is missing a lowercase character",
            extra={
                "error": exc.__class__.__name__,
                "path": str(request.url.path),
                "client": request.client.host if request.client else None,
            }
        )

        return JSONResponse(
            content={
                "error": "password must contain a lowercase character"
            },
            status_code=400
        )

    @app.exception_handler(PasswordMissingUppercaseError)
    async def password_missing_uppercase(
        request: Request,
        exc: PasswordMissingUppercaseError
    ) -> JSONResponse:
        logger.info(
            "Password is missing an uppercase character",
            extra={
                "error": exc.__class__.__name__,
                "path": str(request.url.path),
                "client": request.client.host if request.client else None,
            }
        )

        return JSONResponse(
            content={
                "error": "password must contain an uppercase character"
            },
            status_code=400
        )

    @app.exception_handler(PasswordMissingDigitError)
    async def password_missing_digit(
        request: Request,
        exc: PasswordMissingDigitError
    ) -> JSONResponse:
        logger.info(
            "Password is missing a digit character",
            extra={
                "error": exc.__class__.__name__,
                "path": str(request.url.path),
                "client": request.client.host if request.client else None,
            }
        )

        return JSONResponse(
            content={
                "error": "password must contain a digit"
            },
            status_code=400
        )

    @app.exception_handler(PasswordMissingSpecialCharError)
    async def password_missing_special_character(
        request: Request,
        exc: PasswordMissingSpecialCharError
    ) -> JSONResponse:
        logger.info(
            "Password is missing a special character",
            extra={
                "error": exc.__class__.__name__,
                "path": str(request.url.path),
                "client": request.client.host if request.client else None,
            }
        )

        return JSONResponse(
            content={
                "error": "password must contain a special character"
            },
            status_code=400
        )

    @app.exception_handler(PasswordTooWeakError)
    async def password_too_weak(
        request: Request,
        exc: PasswordTooWeakError
    ) -> JSONResponse:
        logger.info(
            "Password doesn't match strength requirements",
            extra={
                "error": exc.__class__.__name__,
                "path": str(request.url.path),
                "client": request.client.host if request.client else None,
            }
        )

        return JSONResponse(
            content={
                "error": "password doesn't meet strength requirements"
            },
            status_code=400
        )

    @app.exception_handler(PasswordMissmatchError)
    async def password_missmatch(
        request: Request,
        exc: PasswordMissmatchError
    ) -> JSONResponse:
        logger.info(
            "old password doesn't match current password",
            extra={
                "error": exc.__class__.__name__,
                "path": str(request.url.path),
                "client": request.client.host if request.client else None,
            }
        )

        return JSONResponse(
            content={
                "error": "old password does not match the current password"
            },
            status_code=400
        )

    @app.exception_handler(PasswordReuseError)
    async def password_reuse(
        request: Request,
        exc: PasswordReuseError
    ) -> JSONResponse:
        logger.info(
            "new password is the current password",
            extra={
                "error": exc.__class__.__name__,
                "path": str(request.url.path),
                "client": request.client.host if request.client else None,
            }
        )

        return JSONResponse(
            content={
                "error": "password must not be reused"
            },
            status_code=400
        )

    # ------------------------
    # --- Email Exceptions ---
    # ------------------------
    @app.exception_handler(EmailAlreadyExistError)
    async def email_already_exist(
        request: Request,
        exc: EmailAlreadyExistError
    ) -> JSONResponse:
        logger.info(
            "Email change rejected",
            extra={
                "error": exc.__class__.__name__,
                "path": str(request.url.path),
                "client": request.client.host if request.client else None,
            }
        )

        return JSONResponse(
            content={"error": "Email is unavailable"},
            status_code=400
        )

    @app.exception_handler(EmailSpaceError)
    async def email_space_error(
        request: Request,
        exc: EmailSpaceError
    ) -> JSONResponse:
        logger.info(
            "Email contain a space",
            extra={
                "error": exc.__class__.__name__,
                "path": str(request.url.path),
                "client": request.client.host if request.client else None,
            }
        )

        return JSONResponse(
            content={"error": "Email cannot contain a space"},
            status_code=400
        )

    @app.exception_handler(EmailTooShortError)
    async def email_too_short(
        request: Request,
        exc: EmailTooShortError
    ) -> JSONResponse:
        logger.info(
            "Email too short",
            extra={
                "error": exc.__class__.__name__,
                "path": str(request.url.path),
                "client": request.client.host if request.client else None,
            }
        )

        return JSONResponse(
            content={
                "error": "Email must be at least {} character long"
                .format(MIN_EMAIL_LENGTH)
            },
            status_code=400
        )

    @app.exception_handler(EmailTooLongError)
    async def email_too_long(
        request: Request,
        exc: EmailTooLongError
    ) -> JSONResponse:
        logger.info(
            "Email too long",
            extra={
                "error": exc.__class__.__name__,
                "path": str(request.url.path),
                "client": request.client.host if request.client else None,
            }
        )

        return JSONResponse(
            content={
                "error": "Email must be less than {} character long"
                .format(MAX_EMAIL_LENGTH)
            },
            status_code=400
        )

    @app.exception_handler(EmailIsBlankError)
    async def email_is_blank(
        request: Request,
        exc: EmailIsBlankError
    ) -> JSONResponse:
        logger.info(
            "Email is blank",
            extra={
                "error": exc.__class__.__name__,
                "path": str(request.url.path),
                "client": request.client.host if request.client else None,
            }
        )

        return JSONResponse(
            content={
                "error": "Email must not be blank"
            },
            status_code=400
        )

    @app.exception_handler(EmailInvalidDomainError)
    async def email_invalid_domain(
        request: Request,
        exc: EmailInvalidDomainError
    ) -> JSONResponse:
        logger.info(
            "Email domain is invalid",
            extra={
                "error": exc.__class__.__name__,
                "path": str(request.url.path),
                "client": request.client.host if request.client else None,
            }
        )

        return JSONResponse(
            content={
                "error": "Email domain is invalid"
            },
            status_code=400
        )

    @app.exception_handler(EmailInvalidLocalPartError)
    async def email_invalid_local_part(
        request: Request,
        exc: EmailInvalidDomainError
    ) -> JSONResponse:
        logger.info(
            "Email local part is invalid",
            extra={
                "error": exc.__class__.__name__,
                "path": str(request.url.path),
                "client": request.client.host if request.client else None,
            }
        )

        return JSONResponse(
            content={
                "error": "Email local part is invalid"
            },
            status_code=400
        )

    @app.exception_handler(EmailLocalPartTooLongError)
    async def email_local_part_too_long(
        request: Request,
        exc: EmailLocalPartTooLongError
    ) -> JSONResponse:
        logger.info(
            "Email local part is too long",
            extra={
                "error": exc.__class__.__name__,
                "path": str(request.url.path),
                "client": request.client.host if request.client else None,
            }
        )

        return JSONResponse(
            content={
                "error": "Email local part must be less then {} character"
                .format(MAX_LOCAL_PART)
            },
            status_code=400
        )

    @app.exception_handler(EmailInvalidAtCountError)
    async def email_invalid_at_counter(
        request: Request,
        exc: EmailInvalidAtCountError
    ) -> JSONResponse:
        logger.info(
            "Email invalid number of @",
            extra={
                "error": exc.__class__.__name__,
                "path": str(request.url.path),
                "client": request.client.host if request.client else None,
            }
        )

        return JSONResponse(
            content={
                "error": "Email must contain exacly one @"
            },
            status_code=400
        )

    # --------------------------------
    # --- Refresh Token Exceptions ---
    # --------------------------------

    @app.exception_handler(RefreshTokenNotFoundError)
    async def refresh_token_not_found_error(
        request: Request,
        exc: RefreshTokenNotFoundError
    ) -> JSONResponse:
        logger.info(
            "refresh token is missing",
            extra={
                "error": exc.__class__.__name__,
                "path": str(request.url.path),
                "client": request.client.host if request.client else None,
            }
        )

        return JSONResponse(
            content={
                "error": "Refresh token not found"
            },
            status_code=404
        )

    @app.exception_handler(RefreshTokenIsBlankError)
    async def refresh_token_is_blank(
        request: Request,
        exc: RefreshTokenIsBlankError
    ) -> JSONResponse:
        logger.info(
            "refresh token is blank",
            extra={
                "error": exc.__class__.__name__,
                "path": str(request.url.path),
                "client": request.client.host if request.client else None,
            }
        )

        return JSONResponse(
            content={
                "error": "Refresh token must not be blank"
            },
            status_code=400
        )

    @app.exception_handler(RefreshTokenTooShortError)
    async def refresh_token_too_short(
        request: Request,
        exc: RefreshTokenTooShortError
    ) -> JSONResponse:
        logger.info(
            "refresh token is too short",
            extra={
                "error": exc.__class__.__name__,
                "path": str(request.url.path),
                "client": request.client.host if request.client else None,
            }
        )

        return JSONResponse(
            content={
                "error": "Refresh token must be at least {} character long"
                .format(REFRESH_TOKEN_MIN_SIZE)
            },
            status_code=400
        )

    @app.exception_handler(RefreshTokenTooLongError)
    async def refresh_token_too_long(
        request: Request,
        exc: RefreshTokenTooLongError
    ) -> JSONResponse:
        logger.info(
            "refresh token is too short",
            extra={
                "error": exc.__class__.__name__,
                "path": str(request.url.path),
                "client": request.client.host if request.client else None,
            }
        )

        return JSONResponse(
            content={
                "error": "Refresh token must be less than {} character"
                .format(REFRESH_TOKEN_MAX_SIZE)
            },
            status_code=400
        )

    @app.exception_handler(RevokedRefreshTokenError)
    async def refresh_token_is_revoked(
        request: Request,
        exc: RevokedRefreshTokenError
    ) -> JSONResponse:
        logger.info(
            "refresh token is revoked",
            extra={
                "error": exc.__class__.__name__,
                "path": str(request.url.path),
                "client": request.client.host if request.client else None,
            }
        )

        return JSONResponse(
            content={
                "error": "Refresh token is revoked"
            },
            status_code=401
        )

    @app.exception_handler(InvalidRefreshTokenError)
    async def refresh_token_is_invalid(
        request: Request,
        exc: InvalidRefreshTokenError
    ) -> JSONResponse:
        logger.info(
            "refresh token is invalid",
            extra={
                "error": exc.__class__.__name__,
                "path": str(request.url.path),
                "client": request.client.host if request.client else None,
            }
        )

        return JSONResponse(
            content={
                "error": "Refresh token is invalid"
            },
            status_code=400
        )

    @app.exception_handler(ExpiredRefreshTokenError)
    async def refresh_token_is_expired(
        request: Request,
        exc: ExpiredRefreshTokenError
    ) -> JSONResponse:
        logger.info(
            "refresh token is expired",
            extra={
                "error": exc.__class__.__name__,
                "path": str(request.url.path),
                "client": request.client.host if request.client else None,
            }
        )

        return JSONResponse(
            content={
                "error": "Refresh token is expired"
            },
            status_code=401
        )

    # ---------------------
    # --- Me Exception ----
    # ---------------------

    @app.exception_handler(AdminCantSelfDeleteError)
    async def admin_cant_self_delete(
        request: Request,
        exc: AdminCantSelfDeleteError
    ) -> JSONResponse:
        logger.info(
            "admin can't self delete",
            extra={
                "error": exc.__class__.__name__,
                "path": str(request.url.path),
                "client": request.client.host if request.client else None,
            }
        )

        return JSONResponse(
            content={
                "error": "Admin can't self delete"
            },
            status_code=403
        )

    # -----------------------
    # --- Role Exceptions ---
    # -----------------------

    @app.exception_handler(AdminCantSelfRevokeError)
    async def admin_cant_self_revoke(
        request: Request,
        exc: AdminCantSelfRevokeError
    ) -> JSONResponse:
        logger.info(
            "admin can't self revoke",
            extra={
                "error": exc.__class__.__name__,
                "path": str(request.url.path),
                "client": request.client.host if request.client else None,
            }
        )

        return JSONResponse(
            content={
                "error": "Admin can't self revoke"
            },
            status_code=403
        )

    @app.exception_handler(BaseRoleCannotBeRevokedError)
    async def base_role_cannot_be_revoked(
        request: Request,
        exc: BaseRoleCannotBeRevokedError
    ) -> JSONResponse:
        logger.info(
            "base role cannot be revoked",
            extra={
                "error": exc.__class__.__name__,
                "path": str(request.url.path),
                "client": request.client.host if request.client else None,
            }
        )

        return JSONResponse(
            content={
                "error": "Base role cannot be revoked"
            },
            status_code=403
        )

    # ---------------------------
    # --- Disabling Exception ---
    # ---------------------------
    @app.exception_handler(AdminCantSelfDisableError)
    async def admin_self_disable(
        request: Request,
        exc: BaseRoleCannotBeRevokedError
    ) -> JSONResponse:
        logger.info(
            "admin can't disable themselves",
            extra={
                "error": exc.__class__.__name__,
                "path": str(request.url.path),
                "client": request.client.host if request.client else None,
            }
        )

        return JSONResponse(
            content={
                "error": "Admin can't disable themselves"
            },
            status_code=403
        )

    @app.exception_handler(AdminCantSelfRennableError)
    async def admin_self_reenable(
        request: Request,
        exc: AdminCantSelfRennableError
    ) -> JSONResponse:
        logger.info(
            "admin can't reenable themselves",
            extra={
                "error": exc.__class__.__name__,
                "path": str(request.url.path),
                "client": request.client.host if request.client else None,
            }
        )

        return JSONResponse(
            content={
                "error": "Admin can't rennable themselves"
            },
            status_code=403
        )

    @app.exception_handler(AuthUserIsDisabledError)
    async def user_is_disabled(
        request: Request,
        exc: AuthUserIsDisabledError
    ) -> JSONResponse:
        logger.info(
            "user is disabled",
            extra={
                "error": exc.__class__.__name__,
                "path": str(request.url.path),
                "client": request.client.host if request.client else None,
            }
        )

        return JSONResponse(
            content={
                "error": "user is disabled"
            },
            status_code=403
        )
