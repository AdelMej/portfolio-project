from fastapi import FastAPI
from .auth_exception_handler import register_exception_handler as auth_handler
from .common_exception_handler import (
    register_exception_handler as common_handler
)


def register_exception_handlers(app: FastAPI):
    auth_handler(app)
    common_handler(app)
