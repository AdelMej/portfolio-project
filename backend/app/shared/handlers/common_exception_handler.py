from fastapi.applications import FastAPI
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from app.shared.exceptions.commons import (
    UnauthorizedError,
    ForbiddenError,
    NotFoundError
)
import logging

logger = logging.getLogger("app.commons.exceptions")


def register_exception_handler(app: FastAPI):
    @app.exception_handler(UnauthorizedError)
    async def unauthorized(
        request: Request,
        exc: UnauthorizedError
    ) -> JSONResponse:
        logger.info(
            "Unauthorized",
            extra={
                "error": exc.__class__.__name__,
                "path": str(request.url.path),
                "client": request.client.host if request.client else None,
            }
        )

        return JSONResponse(
            content={"error": "Unauthorized"},
            status_code=401
        )

    @app.exception_handler(ForbiddenError)
    async def forbidden(
        request: Request,
        exc: ForbiddenError
    ) -> JSONResponse:
        logger.info(
            "Forbidden",
            extra={
                "error": exc.__class__.__name__,
                "path": str(request.url.path),
                "client": request.client.host if request.client else None,
            }
        )

        return JSONResponse(
            content={"error": "Forbidden"},
            status_code=403
        )

    @app.exception_handler(NotFoundError)
    async def notfound(
        request: Request,
        exc: NotFoundError
    ) -> JSONResponse:
        logger.info(
            "Not Found",
            extra={
                "error": exc.__class__.__name__,
                "path": str(request.url.path),
                "client": request.client.host if request.client else None,
            }
        )

        return JSONResponse(
            content={"error": "Not Found"},
            status_code=404
        )
