from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from app.domain.payment_intent.payment_intent_exceptions import (
    PaymentIntentAlreadyExist
)
import logging


logger = logging.getLogger("app.payment_intent.exceptions")


def register_exception_handler(app: FastAPI):
    @app.exception_handler(PaymentIntentAlreadyExist)
    async def payment_intent_already_exists_handler(
        request: Request,
        exc: PaymentIntentAlreadyExist
    ) -> JSONResponse:
        logger.info(
            "payment intent already exists",
            extra={
                "error": exc.__class__.__name__,
                "path": str(request.url.path),
                "client": request.client.host if request.client else None,
            }
        )

        return JSONResponse(
            content={
                "code": "payment_intent_found",
                "error": "payment intent already exists"},
            status_code=404
        )
