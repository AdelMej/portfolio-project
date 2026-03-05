from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from app.domain.credit.credit_exception import (
    InvalidCreditAmount,
    CreditNegativeError
)
import logging


logger = logging.getLogger("app.credit.exceptions")


def register_exception_handler(app: FastAPI):
    @app.exception_handler(InvalidCreditAmount)
    async def invalid_credit_amount(
        request: Request,
        exc: InvalidCreditAmount
    ) -> JSONResponse:
        logger.info(
            "credit amount cannot be 0",
            extra={
                "error": exc.__class__.__name__,
                "path": str(request.url.path),
                "client": request.client.host if request.client else None,
            }
        )

        return JSONResponse(
            content={
                "code": "invalid_credit_amount",
                "error": "credit amount cannot be 0"
            },
            status_code=400
        )

    @app.exception_handler(CreditNegativeError)
    async def credit_negative_handler(
        request: Request,
        exc: CreditNegativeError
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
            content={
                "code": "credit_is_negative",
                "error": "credit cannot be negative"
            },
            status_code=400
        )
