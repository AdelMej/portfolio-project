from datetime import timedelta
from app.domain.auth.actor_entity import Actor, TokenActor
from app.domain.auth.permission import Permission
from app.domain.auth.permission_rules import ensure_has_permission
from app.domain.auth.refresh_token_entity import NewRefreshTokenEntity
from app.domain.user.user_entity import UserEntity
from app.feature.auth.auth_dto import (
    LoginInputDTO,
)
from app.domain.auth.auth_exceptions import (
    InvalidEmailError,
    InvalidPasswordError,
    UserDisabledError
)
from app.feature.auth.uow.login_uow_port import LoginUoWPort
from app.feature.auth.uow.me_uow_port import MeUoWPort
from app.shared.security.jwt_port import JwtPort
from app.shared.security.password_hasher_port import PasswordHasherPort
from app.shared.security.refresh_token_generator_port import (
    RefreshTokenGeneratorPort
)
from app.shared.security.token_hasher_port import TokenHasherPort
from app.shared.utils.time import utcnow


class AuthService:
    """Application service responsible for authentication workflows.

    This service coordinates user authentication logic, including credential
    verification, refresh token rotation, and access token issuance. It acts
    as the orchestration layer between domain logic, persistence through the
    unit of work, and security-related ports such as hashing and token
    generation.

    The service itself contains no framework-specific logic and relies on
    injected ports and repositories to perform side effects, making it
    suitable for use across different delivery mechanisms (e.g., HTTP APIs,
    background jobs).

    Attributes:
        _uow: Unit of work providing access to authentication repositories and
            transactional boundaries.
    """
    async def login(
        self,
        input: LoginInputDTO,
        existing_refresh: str | None,
        uow: LoginUoWPort,
        refresh_token_ttl: int,
        jwt: JwtPort,
        password_hasher: PasswordHasherPort,
        token_hasher: TokenHasherPort,
        refresh_token_generator: RefreshTokenGeneratorPort
    ) -> tuple[str, str]:
        """Authenticate a user and issue access and refresh tokens.

        This method verifies user credentials, optionally revokes an existing
        refresh token, and issues a new access token along with a newly
        generated refresh token. Refresh tokens are stored in hashed form and
        rotated on login when a valid existing refresh token is provided.

        The refresh token expiration is calculated using the provided TTL
        policy and converted into an absolute expiration timestamp.

        Args:
            input: Login input containing the user's email and password.
            existing_refresh: Optional refresh token obtained from the request
                context. If present and valid, it will be revoked before a new
                refresh token is issued.
            refresh_token_ttl: Time-to-live for the refresh token, in seconds.
            jwt: JWT port used to issue access tokens.
            password_hasher: Password hasher used to verify user credentials.
            token_hasher: Token hasher used to hash refresh tokens prior to
                persistence.
            refresh_token_generator: Generator used to create opaque refresh
                token values.

        Returns:
            A tuple containing:
                - The issued access token.
                - The plain refresh token to be returned to the client.

        Raises:
            InvalidEmailError: If no user exists with the provided email.
            InvalidPasswordError: If the provided password is invalid.
        """
        # normalization
        email = input.email.strip().lower()
        password = input.password.strip()

        if not await uow.auth_read.exist_email(email):
            raise InvalidEmailError()

        user = await uow.auth_read.system_get_user_by_email(email)

        if user is None:
            raise InvalidEmailError()

        if user.disabled_at is not None:
            raise UserDisabledError()

        if not password_hasher.verify(password, user.password_hash):
            raise InvalidPasswordError()

        token = None
        if existing_refresh:
            refresh_hash = token_hasher.hash(existing_refresh)
            token = await uow.auth_read.get_refresh_token(refresh_hash)

        refresh_plain = refresh_token_generator.generate()
        refresh_hash = token_hasher.hash(refresh_plain)

        if token:
            await uow.auth_update.rotate_refresh_token(
                current_token_hash=token.token_hash,
                new_token=NewRefreshTokenEntity(
                    user_id=user.id,
                    token_hash=refresh_hash,
                    expires_at=utcnow() + timedelta(seconds=refresh_token_ttl)
                )
            )
        else:
            await uow.auth_update.rotate_refresh_token(
                current_token_hash=None,
                new_token=NewRefreshTokenEntity(
                    user_id=user.id,
                    token_hash=refresh_hash,
                    expires_at=utcnow() + timedelta(seconds=refresh_token_ttl)
                )
            )

        token_actor = TokenActor(
            id=user.id,
            roles=user.roles,
        )

        return (
            jwt.issue_access_token(
                actor=token_actor
            ),
            refresh_plain
        )

    async def get_me(
        self,
        actor: Actor,
        uow: MeUoWPort,
    ) -> UserEntity:

        ensure_has_permission(actor, Permission.READ_SELF)
        return await uow.me_read_repository.get(actor.id)
