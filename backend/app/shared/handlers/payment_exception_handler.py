from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from app.domain.payment.payment_exception import (
    PaymentProviderError,
    PaymentAlreadyPaidError
)
import logging


logger = logging.getLogger("app.payment.exceptions")


def register_exception_handler(app: FastAPI):
    @app.exception_handler(PaymentProviderError)
    async def payment_provider_handler(
        request: Request,
        exc: PaymentProviderError
    ) -> JSONResponse:
        logger.info(
            "payment provider error",
            extra={
                "error": exc.__class__.__name__,
                "path": str(request.url.path),
                "client": request.client.host if request.client else None,
            }
        )

        return JSONResponse(
            content={"error": "payment provider error"},
            status_code=503
        )

    @app.exception_handler(PaymentAlreadyPaidError)
    async def payment_already_paid_handler(
        request: Request,
        exc: PaymentAlreadyPaidError
    ) -> JSONResponse:
        logger.info(
            "payment is already done",
            extra={
                "error": exc.__class__.__name__,
                "path": str(request.url.path),
                "client": request.client.host if request.client else None,
            }
        )

        return JSONResponse(
            content={"error": "payment is already done"},
            status_code=409
        )
