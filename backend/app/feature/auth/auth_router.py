from fastapi import APIRouter
from app.feature.auth.auth_service import AuthService
from app.feature.auth.auth_dto import (
    LoginInputDTO,
    TokenOutputDTO
)
from app.domain.auth.auth_exceptions import (
    InvalidEmailError,
    InvalidPasswordError,
    InvalidCredentialsError
)
from app.shared.security.jwt_port import JwtPort
from app.shared.security.password_hasher_port import PasswordHasherPort

router = APIRouter(prefix="/auth")


@router.post("/login")
async def login(
    input: LoginInputDTO,
    service: AuthService,
    password_hasher: PasswordHasherPort,
    jwt: JwtPort
) -> TokenOutputDTO:
    try:
        return await service.login(input, jwt, password_hasher)
    except (InvalidEmailError, InvalidPasswordError):
        raise InvalidCredentialsError()
