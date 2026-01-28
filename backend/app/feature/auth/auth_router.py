from fastapi import APIRouter, Depends, Request, Response
from fastapi.security import OAuth2PasswordRequestForm
from app.domain.auth.actor_entity import Actor
from app.feature.auth.auth_dependencies import get_auth_service
from app.feature.auth.auth_service import AuthService
from app.feature.auth.auth_dto import (
    GetMeOutputDTO,
    LoginInputDTO,
    TokenOutputDTO
)
from app.domain.auth.auth_exceptions import (
    InvalidEmailError,
    InvalidPasswordError,
)
from app.feature.auth.auth_exception import InvalidCredentialsError
from app.feature.auth.uow.login_uow_port import LoginUoWPort
from app.feature.auth.uow.me_uow_port import MeUoWPort
from app.infrastructure.persistence.sqlalchemy.provider import (
    get_login_uow,
    get_me_uow
)
from app.infrastructure.security.provider import (
    get_current_actor,
    get_jwt,
    get_password_hasher,
    get_refresh_token_generator,
    get_token_hasher
)
from app.infrastructure.settings.provider import get_refresh_token_ttl
from app.shared.security.jwt_port import JwtPort
from app.shared.security.password_hasher_port import PasswordHasherPort
from app.shared.security.refresh_token_generator_port import (
    RefreshTokenGeneratorPort
)
from app.shared.security.token_hasher_port import TokenHasherPort


router = APIRouter(prefix="/auth")


@router.post(
    path="/login",
    response_model=TokenOutputDTO,
    status_code=200
    )
async def login(
    input: LoginInputDTO,
    request: Request,
    response: Response,
    login_uow: LoginUoWPort = Depends(get_login_uow),
    service: AuthService = Depends(get_auth_service),
    password_hasher: PasswordHasherPort = Depends(get_password_hasher),
    jwt: JwtPort = Depends(get_jwt),
    token_hasher: TokenHasherPort = Depends(get_token_hasher),
    refresh_token_generator: RefreshTokenGeneratorPort = Depends(
        get_refresh_token_generator
    ),
    refresh_ttl: int = Depends(get_refresh_token_ttl),
) -> TokenOutputDTO:
    """
    Authenticate a user and return an access token.

    A refresh token is issued and stored in an HTTP-only cookie.
    """
    existing_refresh = request.cookies.get("refresh_token")
    try:
        access, refresh = await service.login(
            input=input,
            existing_refresh=existing_refresh,
            uow=login_uow,
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


@router.post("/token", include_in_schema=False)
async def token(
    request: Request,
    response: Response,
    form: OAuth2PasswordRequestForm = Depends(),
    login_uow: LoginUoWPort = Depends(get_login_uow),
    service: AuthService = Depends(get_auth_service),
    password_hasher: PasswordHasherPort = Depends(get_password_hasher),
    jwt: JwtPort = Depends(get_jwt),
    token_hasher: TokenHasherPort = Depends(get_token_hasher),
    refresh_token_generator: RefreshTokenGeneratorPort = Depends(
        get_refresh_token_generator
    ),
    refresh_ttl: int = Depends(get_refresh_token_ttl),
) -> TokenOutputDTO:
    """
    Authenticate a user and return an access token.

    A refresh token is issued and stored in an HTTP-only cookie.
    """
    existing_refresh = request.cookies.get("refresh_token")

    try:
        input = LoginInputDTO(
            email=form.username,
            password=form.password
        )

        access, refresh = await service.login(
            input=input,
            existing_refresh=existing_refresh,
            uow=login_uow,
            jwt=jwt,
            token_hasher=token_hasher,
            refresh_token_generator=refresh_token_generator,
            refresh_token_ttl=refresh_ttl,
            password_hasher=password_hasher
        )
    except (InvalidEmailError, InvalidPasswordError, ValueError):
        raise InvalidCredentialsError()

    response.set_cookie(
        key="refresh_token",
        value=refresh,
        httponly=True,
        secure=True,
        samesite="lax",
        path="/auth",
        max_age=refresh_ttl
    )

    return TokenOutputDTO(
        access_token=access,
        token_type="bearer"
    )


@router.get(
    "/me",
    response_model=GetMeOutputDTO,
    status_code=200
)
async def me(
    uow: MeUoWPort = Depends(get_me_uow),
    actor: Actor = Depends(get_current_actor),
    service: AuthService = Depends(get_auth_service)
):
    user = await service.get_me(actor, uow)
    return GetMeOutputDTO(
        email=user.email,
        roles=user.roles
    )
