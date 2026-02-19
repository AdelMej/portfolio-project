from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from app.domain.session.session_exception import (
    SessionAttendanceNotOpenError,
    SessionAlreadyAttendedError,
    AlreadyActiveParticipationError,
    SessionCancelledError,
    NotOwnerOfSessionError,
    SessionNotFinishedError,
    SessionNotFoundError,
    InvalidAttendanceInputError,
    SessionOverlappingError,
    SessionTitleIsBlankError,
    SessionTitleTooLongError,
    SessionTitleTooShortError,
    SessionIsFullError,
    SessionClosedForRegistration,
    OwnerCantRegisterToOwnSessionError,
    SessionTimeIsInvalidError,
    SessionCreditNegativeError,
    SessionPriceIsNegativeError,
    NoActiveParticipationFoundError,
    InvalidCoachAccountError
)
import logging
from app.shared.rules.session_title_rules import (
    MAX_TITLE_LENGTH,
    MIN_TITLE_LENGTH
)

logger = logging.getLogger("app.session.exceptions")


def register_exception_handler(app: FastAPI):
    @app.exception_handler(SessionAttendanceNotOpenError)
    async def session_attendance_not_open(
        request: Request,
        exc: SessionAttendanceNotOpenError
    ) -> JSONResponse:
        logger.info(
            "session attendance is not available",
            extra={
                "error": exc.__class__.__name__,
                "path": str(request.url.path),
                "client": request.client.host if request.client else None,
            }
        )

        return JSONResponse(
            content={
                "error": "session attendance is not available"
            },
            status_code=403
        )

    @app.exception_handler(SessionAlreadyAttendedError)
    async def session_already_attended_handler(
        request: Request,
        exc: SessionAlreadyAttendedError
    ) -> JSONResponse:
        logger.info(
            "session attendance is already done",
            extra={
                "error": exc.__class__.__name__,
                "path": str(request.url.path),
                "client": request.client.host if request.client else None,
            }
        )

        return JSONResponse(
            content={"error": "session attendance is already done"},
            status_code=409
        )

    @app.exception_handler(AlreadyActiveParticipationError)
    async def already_active_participation_handler(
        request: Request,
        exc: AlreadyActiveParticipationError
    ) -> JSONResponse:
        logger.info(
            "user is already registered for that session",
            extra={
                "error": exc.__class__.__name__,
                "path": str(request.url.path),
                "client": request.client.host if request.client else None,
            }
        )

        return JSONResponse(
            content={"error": "user is already registered for that session"},
            status_code=409
        )

    @app.exception_handler(SessionCancelledError)
    async def session_cancelled_handler(
        request: Request,
        exc: SessionCancelledError
    ) -> JSONResponse:
        logger.info(
            "session is cancelled",
            extra={
                "error": exc.__class__.__name__,
                "path": str(request.url.path),
                "client": request.client.host if request.client else None,
            }
        )

        return JSONResponse(
            content={"error": "session is cancelled"},
            status_code=409
        )

    @app.exception_handler(NotOwnerOfSessionError)
    async def not_owner_of_session_handler(
        request: Request,
        exc: NotOwnerOfSessionError
    ) -> JSONResponse:
        logger.info(
            "coach doesn't own the session",
            extra={
                "error": exc.__class__.__name__,
                "path": str(request.url.path),
                "client": request.client.host if request.client else None,
            }
        )

        return JSONResponse(
            content={"error": "coach doesn't own the session"},
            status_code=403
        )

    @app.exception_handler(SessionNotFoundError)
    async def session_not_found_handler(
        request: Request,
        exc: SessionNotFoundError
    ) -> JSONResponse:
        logger.info(
            "session not found",
            extra={
                "error": exc.__class__.__name__,
                "path": str(request.url.path),
                "client": request.client.host if request.client else None,
            }
        )

        return JSONResponse(
            content={"error": "session not found"},
            status_code=404
        )

    @app.exception_handler(InvalidAttendanceInputError)
    async def invalid_attendance_input_handler(
        request: Request,
        exc: InvalidAttendanceInputError
    ) -> JSONResponse:
        logger.info(
            "invalid attendance input",
            extra={
                "error": exc.__class__.__name__,
                "path": str(request.url.path),
                "client": request.client.host if request.client else None,
            }
        )

        return JSONResponse(
            content={"error": "invalid attendance input"},
            status_code=400
     )

    @app.exception_handler(SessionOverlappingError)
    async def session_overlapping_handler(
        request: Request,
        exc: SessionOverlappingError
    ) -> JSONResponse:
        logger.info(
            "session is overlapping",
            extra={
                "error": exc.__class__.__name__,
                "path": str(request.url.path),
                "client": request.client.host if request.client else None,
            }
        )

        return JSONResponse(
            content={"error": "session is overlapping"},
            status_code=409
        )

    @app.exception_handler(SessionTitleIsBlankError)
    async def session_title_is_blank_handler(
        request: Request,
        exc: SessionTitleIsBlankError
    ) -> JSONResponse:
        logger.info(
            "title is blank",
            extra={
                "error": exc.__class__.__name__,
                "path": str(request.url.path),
                "client": request.client.host if request.client else None,
            }
        )

        return JSONResponse(
            content={"error": "title is blank"},
            status_code=400
        )

    @app.exception_handler(SessionTitleTooShortError)
    async def session_title_too_short_handler(
        request: Request,
        exc: SessionTitleTooShortError
    ) -> JSONResponse:
        logger.info(
            "title must be at least {} characters long"
            .format(MIN_TITLE_LENGTH),
            extra={
                "error": exc.__class__.__name__,
                "path": str(request.url.path),
                "client": request.client.host if request.client else None,
            }
        )

        return JSONResponse(
            content={
                "error": "title must be at least {} characters long"
                .format(MIN_TITLE_LENGTH)
            },
            status_code=400
        )

    @app.exception_handler(SessionTitleTooLongError)
    async def session_title_too_long_handler(
        request: Request,
        exc: SessionTitleTooLongError
    ) -> JSONResponse:
        logger.info(
            "title must be less than {} characters long"
            .format(MAX_TITLE_LENGTH),
            extra={
                "error": exc.__class__.__name__,
                "path": str(request.url.path),
                "client": request.client.host if request.client else None,
            }
        )

        return JSONResponse(
            content={
                "error": "title must be less than {} characters long"
                .format(MAX_TITLE_LENGTH)
            },
            status_code=409
        )

    @app.exception_handler(SessionIsFullError)
    async def session_is_full_handler(
        request: Request,
        exc: SessionIsFullError
    ) -> JSONResponse:
        logger.info(
            "session is full",
            extra={
                "error": exc.__class__.__name__,
                "path": str(request.url.path),
                "client": request.client.host if request.client else None,
            }
        )

        return JSONResponse(
            content={"error": "session is full"},
            status_code=409
        )

    @app.exception_handler(SessionClosedForRegistration)
    async def session_close_for_registration_handler(
        request: Request,
        exc: SessionCancelledError
    ) -> JSONResponse:
        logger.info(
            "session registration is closed",
            extra={
                "error": exc.__class__.__name__,
                "path": str(request.url.path),
                "client": request.client.host if request.client else None,
            }
        )

        return JSONResponse(
            content={"error": "session registration is closed"},
            status_code=403
        )

    @app.exception_handler(OwnerCantRegisterToOwnSessionError)
    async def owner_self_registration_handler(
        request: Request,
        exc: OwnerCantRegisterToOwnSessionError
    ) -> JSONResponse:
        logger.info(
            "session owner",
            extra={
                "error": exc.__class__.__name__,
                "path": str(request.url.path),
                "client": request.client.host if request.client else None,
            }
        )

        return JSONResponse(
            content={"error": "session owner"},
            status_code=409
        )

    @app.exception_handler(SessionTimeIsInvalidError)
    async def session_time_is_invalid_handler(
        request: Request,
        exc: SessionTimeIsInvalidError
    ) -> JSONResponse:
        logger.info(
            "invalid session time",
            extra={
                "error": exc.__class__.__name__,
                "path": str(request.url.path),
                "client": request.client.host if request.client else None,
            }
        )

        return JSONResponse(
            content={"error": "invalid session time"},
            status_code=400
        )

    @app.exception_handler(SessionCreditNegativeError)
    async def session_credit_is_negative_handler(
        request: Request,
        exc: SessionCreditNegativeError
    ) -> JSONResponse:
        logger.info(
            "credit cannot be negative",
            extra={
                "error": exc.__class__.__name__,
                "path": str(request.url.path),
                "client": request.client.host if request.client else None,
            }
        )

        return JSONResponse(
            content={"error": "credit cannot be negative"},
            status_code=400
        )

    @app.exception_handler(SessionPriceIsNegativeError)
    async def session_price_is_negative_handler(
        request: Request,
        exc: SessionPriceIsNegativeError
    ) -> JSONResponse:
        logger.info(
            "price cannot be negative",
            extra={
                "error": exc.__class__.__name__,
                "path": str(request.url.path),
                "client": request.client.host if request.client else None,
            }
        )

        return JSONResponse(
            content={"error": "price cannot be negative"},
            status_code=400
        )

    @app.exception_handler(NoActiveParticipationFoundError)
    async def no_active_paritcipation_found_handler(
        request: Request,
        exc: NoActiveParticipationFoundError
    ) -> JSONResponse:
        logger.info(
            "no active participation found",
            extra={
                "error": exc.__class__.__name__,
                "path": str(request.url.path),
                "client": request.client.host if request.client else None,
            }
        )

        return JSONResponse(
            content={"error": "no active participation found"},
            status_code=404
        )

    @app.exception_handler(InvalidCoachAccountError)
    async def invalid_coach_account_error(
        request: Request,
        exc: InvalidCoachAccountError
    ) -> JSONResponse:
        logger.info(
            "stripe account is invalid",
            extra={
                "error": exc.__class__.__name__,
                "path": str(request.url.path),
                "client": request.client.host if request.client else None,
            }
        )

        return JSONResponse(
            content={"error": "stripe account is invalid"},
            status_code=400
        )
    @app.exception_handler(SessionNotFinishedError)
    async def session_not_finished_error(
        request: Request,
        exc: SessionNotFinishedError
    ) -> JSONResponse:
        logger.info(
            "session is not finished",
            extra={
                "error": exc.__class__.__name__,
                "path": str(request.url.path),
                "client": request.client.host if request.client else None,
            }
        )

        return JSONResponse(
            content={"error": "session is not finished"},
            status_code=409
        )
