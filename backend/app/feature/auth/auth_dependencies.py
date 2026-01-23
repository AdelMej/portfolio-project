from fastapi.param_functions import Depends
from app.feature.auth.auth_service import AuthService
from app.feature.auth.auth_UoW_port import AuthUoW
from app.infrastructure.persistence.in_memory.provider import (
    get_in_memory_auth_uow
)


def get_auth_service(uow: AuthUoW = Depends(get_in_memory_auth_uow)):
    return AuthService(uow=uow)
