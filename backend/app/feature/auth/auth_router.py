from fastapi import APIRouter, Depends, Request, Response
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
from app.infrastructure.security.provider import get_refresh_token_generator
from app.shared.security.jwt_port import JwtPort
from app.shared.security.password_hasher_port import PasswordHasherPort
from fastapi.security import OAuth2PasswordBearer
from app.feature.auth.auth_dependencies import get_auth_service
from app.infrastructure.security.in_memory.provider import (
    get_in_memory_jwt,
    get_in_memory_password_hasher,
    get_in_memory_token_hasher
)
from app.infrastructure.settings.provider import get_refresh_token_ttl
from app.shared.security.refresh_token_geneartor_port import (
    RefreshTokenGeneratorPort
)
from app.shared.security.token_hasher_port import TokenHasherPort

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

router = APIRouter(prefix="/auth")


@router.post("/login")
async def login(
    input: LoginInputDTO,
    request: Request,
    response: Response,
    service: AuthService = Depends(get_auth_service),
    password_hasher: PasswordHasherPort = Depends(
        get_in_memory_password_hasher
    ),
    jwt: JwtPort = Depends(get_in_memory_jwt),
    token_hasher: TokenHasherPort = Depends(get_in_memory_token_hasher),
    refresh_token_generator: RefreshTokenGeneratorPort = Depends(
        get_refresh_token_generator
    ),
    refresh_ttl: int = Depends(get_refresh_token_ttl)
) -> TokenOutputDTO:
    existing_refresh = request.cookies.get("refresh_token")

    try:
        access, refresh = await service.login(
            input=input,
            existing_refresh=existing_refresh,
            jwt=jwt,
            token_hasher=token_hasher,
            refresh_token_generator=refresh_token_generator,
            refresh_token_ttl=refresh_ttl,
            password_hasher=password_hasher
        )
    except (InvalidEmailError, InvalidPasswordError):
        raise InvalidCredentialsError()

    response.set_cookie(
        key="refresh_token",
        value=refresh,
        httponly=True,
        secure=True,
        samesite="lax",
        path="/refresh",
        max_age=refresh_ttl
    )

    return TokenOutputDTO(
        access_token=access,
        token_type="bearer"
    )


@router.get("/me")
async def me(token: str = Depends(oauth2_scheme)):
    return {"token": token}
