from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import logging

from app.domain.auth.auth_exceptions import EmailAlreadyExistError
from app.feature.auth.auth_exception import (
    InvalidTokenError,
    InvalidCredentialsError
)

logger = logging.getLogger("app.exceptions")


def register_exception_handler(app: FastAPI):

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

    @app.exception_handler(EmailAlreadyExistError)
    async def email_already_exist(
        request: Request,
        exc: InvalidCredentialsError
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
            status_code=401
        )
