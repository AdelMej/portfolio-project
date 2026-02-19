from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.responses import JSONResponse
import logging
from app.domain.stripe.stripe_exception import (
    ChargeNotReadyError,
    IntentIsInvalidError,
    BalanceNotExpendedError,
    CoachPayoutFailedError
)

logger = logging.getLogger("app.session.exceptions")


def register_exception_handler(app: FastAPI):
    @app.exception_handler(ChargeNotReadyError)
    async def charge_not_ready_handler(
        request: Request,
        exc: ChargeNotReadyError
    ) -> JSONResponse:
        logger.info(
            "charge is not ready",
            extra={
                "error": exc.__class__.__name__,
                "path": str(request.url.path),
                "client": request.client.host if request.client else None,
            }
        )

        return JSONResponse(
            content={"error": "charge is not ready"},
            status_code=503
        )

    @app.exception_handler(IntentIsInvalidError)
    async def intent_is_invalid_handler(
        request: Request,
        exc: IntentIsInvalidError
    ) -> JSONResponse:
        logger.info(
            "intent is invalid",
            extra={
                "error": exc.__class__.__name__,
                "path": str(request.url.path),
                "client": request.client.host if request.client else None,
            }
        )

        return JSONResponse(
            content={"error": "intent is invalid"},
            status_code=503
        )

    @app.exception_handler(BalanceNotExpendedError)
    async def balance_not_expended_handler(
        request: Request,
        exc: BalanceNotExpendedError
    ) -> JSONResponse:
        logger.info(
            "balance is not expended",
            extra={
                "error": exc.__class__.__name__,
                "path": str(request.url.path),
                "client": request.client.host if request.client else None,
            }
        )

        return JSONResponse(
            content={"error": "balance is not expended"},
            status_code=503
        )

    @app.exception_handler(CoachPayoutFailedError)
    async def coach_payout_failed_handler(
        request: Request,
        exc: CoachPayoutFailedError
    ) -> JSONResponse:
        logger.info(
            "payout failed",
            extra={
                "error": exc.__class__.__name__,
                "path": str(request.url.path),
                "client": request.client.host if request.client else None,
            }
        )

        return JSONResponse(
            content={"error": "payout failed"},
            status_code=400
        )
