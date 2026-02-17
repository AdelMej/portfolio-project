import logging

from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from app.domain.currency.currency_exception import (
    CurrencyInvalidLengthError,
    CurrencyInvalidFormatError
)
from app.shared.rules.currency_rules import (
    CURRENCY_LENGTH
)

logger = logging.getLogger("app.currency.exceptions")


def register_exception_handler(app: FastAPI):
    @app.exception_handler(CurrencyInvalidLengthError)
    async def currency_invalid_length_handler(
        request: Request,
        exc: CurrencyInvalidLengthError
    ) -> JSONResponse:
        logger.info(
            "currency must be {} characters long"
            .format(CURRENCY_LENGTH),
            extra={
                "error": exc.__class__.__name__,
                "path": str(request.url.path),
                "client": request.client.host if request.client else None,
            }
        )

        return JSONResponse(
            content={
                "error": "currency must be {} characters long"
                .format(CURRENCY_LENGTH)
            },
            status_code=400
        )

    @app.exception_handler(CurrencyInvalidFormatError)
    async def currency_invalid_format_handler(
        request: Request,
        exc: CurrencyInvalidFormatError
    ) -> JSONResponse:
        logger.info(
            "currency format is invalid",
            extra={
                "error": exc.__class__.__name__,
                "path": str(request.url.path),
                "client": request.client.host if request.client else None,
            }
        )

        return JSONResponse(
            content={"error": "currency fromat is invalid"},
            status_code=400
        )
