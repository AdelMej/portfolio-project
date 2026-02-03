from fastapi import APIRouter, Depends, Request, Response
from fastapi.security import OAuth2PasswordRequestForm
from app.domain.auth.actor_entity import Actor
from app.domain.user.user_profile_entity import UserProfileEntity
from app.feature.auth.auth_dependencies import get_auth_service
from app.feature.auth.auth_service import AuthService
from app.feature.auth.auth_dto import (
    GetMeOutputDTO,
    GetMeProfileOutputDTO,
    LoginInputDTO,
    MePasswordChangeInputDTO,
    RegistrationInputDTO,
    TokenOutputDTO,
    MeEmailChangeInputDTO,
    UpdateMeProfileInputDTO,
)
from app.domain.auth.auth_exceptions import (
    AuthDomainError,
    EmailAlreadyExistError,
    InvalidEmailError,
    InvalidPasswordError,
    PermissionDeniedError,
)
from app.feature.auth.auth_exception import (
    InvalidCredentialsError,
    InvalidTokenError,
    RegistrationFailed
)
from app.feature.auth.uow.login_uow_port import LoginUoWPort
from app.feature.auth.uow.logout_uow_port import LogoutUoWPort
from app.feature.auth.uow.me_uow_port import MeUoWPort
from app.feature.auth.uow.refresh_uow_port import RefreshTokenUoWPort
from app.feature.auth.uow.registration_uow_port import RegistrationUoWPort
from app.infrastructure.persistence.sqlalchemy.provider import (
    get_login_uow,
    get_logout_uow,
    get_me_uow,
    get_refresh_uow,
    get_registration_uow
)
from app.infrastructure.security.provider import (
    get_current_actor,
    get_jwt,
    get_password_hasher,
    get_token_generator,
    get_token_hasher
)
from app.infrastructure.settings.provider import get_refresh_token_ttl
from app.shared.exceptions.commons import UnauthorizedError
from app.shared.security.jwt_port import JwtPort
from app.shared.security.password_hasher_port import PasswordHasherPort
from app.shared.security.token_generator_port import (
    TokenGeneratorPort
)
from app.shared.security.token_hasher_port import TokenHasherPort
from app.shared.exceptions.commons import ForbiddenError
import logging


logger = logging.getLogger("app.auth")

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)


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
    token_generator: TokenGeneratorPort = Depends(
        get_token_generator
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
            token_generator=token_generator,
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
    uow: LoginUoWPort = Depends(get_login_uow),
    service: AuthService = Depends(get_auth_service),
    password_hasher: PasswordHasherPort = Depends(get_password_hasher),
    jwt: JwtPort = Depends(get_jwt),
    token_hasher: TokenHasherPort = Depends(get_token_hasher),
    refresh_token_generator: TokenGeneratorPort = Depends(
        get_token_generator
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
            uow=uow,
            jwt=jwt,
            token_hasher=token_hasher,
            token_generator=refresh_token_generator,
            refresh_token_ttl=refresh_ttl,
            password_hasher=password_hasher
        )
    except (InvalidEmailError, InvalidPasswordError, ValueError) as e:
        logger.info(
            e.__class__.__name__
        )
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


@router.post(
    path="/refresh",
    response_model=TokenOutputDTO,
    status_code=200
)
async def refresh(
    request: Request,
    response: Response,
    uow: RefreshTokenUoWPort = Depends(get_refresh_uow),
    jwt: JwtPort = Depends(get_jwt),
    service: AuthService = Depends(get_auth_service),
    token_hasher: TokenHasherPort = Depends(get_token_hasher),
    token_generator: TokenGeneratorPort = Depends(get_token_generator),
    refresh_ttl: int = Depends(get_refresh_token_ttl)
) -> TokenOutputDTO:
    current_refresh = request.cookies.get("refresh_token")

    if current_refresh is None:
        raise UnauthorizedError()

    try:
        access, refresh = await service.refresh(
            current_refresh_token=current_refresh,
            uow=uow,
            jwt=jwt,
            token_hasher=token_hasher,
            token_generator=token_generator,
            refresh_ttl=refresh_ttl,
        )
    except AuthDomainError as e:
        logger.info(
            e.__class__.__name__
        )
        raise InvalidTokenError()

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


@router.put(
    path="/register",
    status_code=204
)
async def register(
    input: RegistrationInputDTO,
    uow: RegistrationUoWPort = Depends(get_registration_uow),
    password_hasher: PasswordHasherPort = Depends(get_password_hasher),
    service: AuthService = Depends(get_auth_service)
):
    try:
        await service.register(
            input=input,
            uow=uow,
            password_hasher=password_hasher,
        )
    except EmailAlreadyExistError:
        raise RegistrationFailed()


@router.post(
    path="/logout",
    status_code=204
)
async def logout(
    request: Request,
    response: Response,
    uow: LogoutUoWPort = Depends(get_logout_uow),
    service: AuthService = Depends(get_auth_service),
    token_hasher: TokenHasherPort = Depends(get_token_hasher)
) -> None:
    refresh_token = request.cookies.get("refresh_token")

    if refresh_token is None:
        return

    await service.logout(
        token=refresh_token,
        uow=uow,
        token_hasher=token_hasher
    )

    response.delete_cookie(
        key="refresh_token",
        path="/auth"
    )


@router.get(
    "/me",
    response_model=GetMeOutputDTO,
    status_code=200
)
async def get_me(
    uow: MeUoWPort = Depends(get_me_uow),
    actor: Actor = Depends(get_current_actor),
    service: AuthService = Depends(get_auth_service)
) -> GetMeOutputDTO:
    try:
        user = await service.get_me(actor, uow)
    except PermissionDeniedError:
        raise ForbiddenError()

    return GetMeOutputDTO(
        email=user.email,
        roles=user.roles
    )


@router.patch(
    "/me/email-change",
    status_code=204
)
async def email_change_me(
    input: MeEmailChangeInputDTO,
    uow: MeUoWPort = Depends(get_me_uow),
    actor: Actor = Depends(get_current_actor),
    service: AuthService = Depends(get_auth_service)
) -> None:
    await service.email_change_me(actor, uow, input)


@router.patch(
    "/me/password-change",
    status_code=204
)
async def password_change_me(
    input: MePasswordChangeInputDTO,
    password_hasher: PasswordHasherPort = Depends(get_password_hasher),
    uow: MeUoWPort = Depends(get_me_uow),
    actor: Actor = Depends(get_current_actor),
    service: AuthService = Depends(get_auth_service)
) -> None:

    await service.password_change_me(
        input=input,
        password_hasher=password_hasher,
        actor=actor,
        uow=uow,
    )


@router.get(
    "/me/profile",
    status_code=200,
    response_model=GetMeProfileOutputDTO
)
async def get_me_profile(
    actor: Actor = Depends(get_current_actor),
    uow: MeUoWPort = Depends(get_me_uow),
    service: AuthService = Depends(get_auth_service)
) -> GetMeProfileOutputDTO:

    user_profile: UserProfileEntity = await service.get_me_profile(
        actor=actor,
        uow=uow
    )

    return GetMeProfileOutputDTO(
        first_name=user_profile.first_name,
        last_name=user_profile.last_name
    )


@router.put(
    "/me/profile",
    status_code=204
)
async def update_me_profile(
    input: UpdateMeProfileInputDTO,
    actor: Actor = Depends(get_current_actor),
    uow: MeUoWPort = Depends(get_me_uow),
    service: AuthService = Depends(get_auth_service)
) -> None:

    await service.update_me_profile(
        input=input,
        actor=actor,
        uow=uow
    )


@router.delete(
    "/me",
    status_code=204
)
async def delete_me(
    response: Response,
    actor: Actor = Depends(get_current_actor),
    uow: MeUoWPort = Depends(get_me_uow),
    refresh_uow: RefreshTokenUoWPort = Depends(get_refresh_uow),
    service: AuthService = Depends(get_auth_service),
    password_hasher: PasswordHasherPort = Depends(get_password_hasher)
) -> None:

    await service.delete_me(
        actor=actor,
        refresh_uow=refresh_uow,
        uow=uow,
        password_hasher=password_hasher,
    )

    response.delete_cookie(
        key="refresh_token",
        path="/auth"
    )
