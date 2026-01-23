from fastapi import Request
from app.infrastructure.settings.app_settings import AppSettings


def get_settings(request: Request) -> AppSettings:
    return request.app.state.settings


def get_refresh_token_ttl(request: Request) -> int:
    return request.app.state.settings.jwt_refresh_ttl_seconds


def get_access_token_ttl(request: Request) -> int:
    return request.app.state.settings.jwt_access_ttl_seconds


def get_jwt_algorithm(request: Request) -> str:
    return request.app.state.settings.jwt_algorithm


def get_jwt_secret(request: Request) -> str:
    return request.app.state.settings.jwt_secret
