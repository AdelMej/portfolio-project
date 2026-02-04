from datetime import timedelta
import secrets
from app.domain.auth.actor_entity import Actor, TokenActor
from app.domain.auth.permission import Permission
from app.domain.auth.permission_rules import ensure_has_permission
from app.domain.auth.refresh_token_entity import (
    NewRefreshTokenEntity,
)
from app.domain.auth.refresh_tokens_rules import (
    ensure_refresh_token_is_valid
)
from app.domain.auth.role import Role
from app.domain.user.user_entity import NewUserEntity, UserEntity
from app.domain.user.user_profile_entity import UserProfileEntity
from app.domain.user.user_profile_rules import (
    ensure_first_name_is_valid,
    ensure_last_name_is_valid
)
from app.feature.auth.auth_dto import (
    LoginInputDTO,
    MeEmailChangeInputDTO,
    MePasswordChangeInputDTO,
    RegistrationInputDTO,
    UpdateMeProfileInputDTO,
)
from app.domain.auth.auth_exceptions import (
    AdminCantSelfDeleteError,
    EmailAlreadyExistError,
    ExpiredRefreshTokenError,
    InvalidEmailError,
    InvalidPasswordError,
    InvalidRefreshTokenError,
    PasswordMissmatchError,
    PasswordReuseError,
    RevokedRefreshTokenError,
    UserDisabledError
)
from app.feature.auth.uow.auth_uow_port import AuthUoWPort
from app.feature.auth.uow.me_uow_port import MeUoWPort
from app.shared.exceptions.runtime import InvariantViolationError
from app.shared.security.jwt_port import JwtPort
from app.shared.security.password_hasher_port import PasswordHasherPort
from app.shared.security.token_generator_port import (
    TokenGeneratorPort
)
from app.shared.security.token_hasher_port import TokenHasherPort
from app.shared.utils.time import utcnow
from app.domain.auth.auth_password_rules import ensure_password_is_strong
from app.domain.auth.auth_email_rules import ensure_email_is_valid


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
    """
    async def login(
        self,
        input: LoginInputDTO,
        existing_refresh: str | None,
        uow: AuthUoWPort,
        refresh_token_ttl: int,
        jwt: JwtPort,
        password_hasher: PasswordHasherPort,
        token_hasher: TokenHasherPort,
        token_generator: TokenGeneratorPort
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

        if not await uow.auth_read_repository.exist_email(email):
            raise InvalidEmailError()

        user = await uow.auth_read_repository.get_user_by_email(email)

        if user is None:
            raise InvalidEmailError()

        if user.disabled_at is not None:
            raise UserDisabledError()

        if not password_hasher.verify(password, user.password_hash):
            raise InvalidPasswordError()

        token = None
        if existing_refresh:
            refresh_hash = token_hasher.hash(existing_refresh)
            token = await uow.auth_read_repository.get_refresh_token(refresh_hash)

        refresh_plain = token_generator.generate()
        refresh_hash = token_hasher.hash(refresh_plain)

        if token:
            await uow.auth_update_repository.rotate_refresh_token(
                current_token_hash=token.token_hash,
                new_token=NewRefreshTokenEntity(
                    user_id=user.id,
                    token_hash=refresh_hash,
                    expires_at=utcnow() + timedelta(seconds=refresh_token_ttl)
                )
            )
        else:
            await uow.auth_update_repository.rotate_refresh_token(
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

    async def refresh(
        self,
        current_refresh_token: str,
        uow: AuthUoWPort,
        jwt: JwtPort,
        token_hasher: TokenHasherPort,
        token_generator: TokenGeneratorPort,
        refresh_ttl: int,
    ) -> tuple[str, str]:
        ensure_refresh_token_is_valid(current_refresh_token)

        current_refresh_hash = token_hasher.hash(current_refresh_token)
        current_refresh = await uow.auth_read_repository.get_refresh_token(
            current_refresh_hash
        )

        if current_refresh is None:
            raise InvalidRefreshTokenError()

        if current_refresh.is_expired():
            raise ExpiredRefreshTokenError()

        if current_refresh.is_revoked():
            raise RevokedRefreshTokenError()

        user = await uow.auth_read_repository.get_user_by_id(current_refresh.user_id)

        if user is None:
            raise InvariantViolationError(
                "Refresh token references missing user",
                context={
                    "refresh_token_hash": current_refresh.token_hash,
                    "user_id": current_refresh.user_id,
                }
            )

        new_token_plain = token_generator.generate()
        new_token_hash = token_hasher.hash(new_token_plain)

        new_refresh_token = NewRefreshTokenEntity(
            user_id=user.id,
            token_hash=new_token_hash,
            expires_at=utcnow() + timedelta(seconds=refresh_ttl)
        )

        await uow.auth_update_repository.rotate_refresh_token(
            current_token_hash=current_refresh_hash,
            new_token=new_refresh_token
        )

        token_actor = TokenActor(
            id=user.id,
            roles=user.roles,
        )

        access_token = jwt.issue_access_token(
            actor=token_actor
        )

        return access_token, new_token_plain

    async def logout(
        self,
        token: str,
        uow: AuthUoWPort,
        token_hasher: TokenHasherPort,
    ) -> None:
        token_hash = token_hasher.hash(token)

        await uow.auth_update_repository.revoke_refresh_token(token_hash)

    async def register(
        self,
        input: RegistrationInputDTO,
        uow: AuthUoWPort,
        password_hasher: PasswordHasherPort,
    ) -> None:
        # normalization
        email = input.email.strip().lower()
        password = input.password.strip()
        first_name = input.first_name.strip()
        last_name = input.last_name.strip()

        ensure_password_is_strong(password)
        ensure_email_is_valid(email)
        ensure_first_name_is_valid(first_name)
        ensure_last_name_is_valid(last_name)

        if await uow.auth_read.exist_email(email):
            raise EmailAlreadyExistError()

        new_user = NewUserEntity(
            email=email,
            password_hash=password_hasher.hash(password),
            role=Role.USER
        )

        new_user_profile = UserProfileEntity(
            first_name=first_name,
            last_name=last_name
        )

        await uow.auth_creation_repository.register(new_user, new_user_profile)

    async def get_me(
        self,
        actor: Actor,
        uow: MeUoWPort,
    ) -> UserEntity:

        ensure_has_permission(actor, Permission.READ_SELF)
        return await uow.me_read_repository.get(actor.id)

    async def email_change_me(
        self,
        actor: Actor,
        uow: MeUoWPort,
        input: MeEmailChangeInputDTO,
    ) -> None:
        ensure_has_permission(actor, Permission.UPDATE_SELF)

        # normalization
        email = input.email.strip().lower()

        if await uow.auth_read_repository.exist_email(email):
            raise EmailAlreadyExistError()

        await uow.me_update_repository.update_email_by_user_id(
            email,
            actor.id
        )

    async def password_change_me(
        self,
        input: MePasswordChangeInputDTO,
        password_hasher: PasswordHasherPort,
        actor: Actor,
        uow: MeUoWPort
    ) -> None:
        ensure_has_permission(actor, Permission.UPDATE_SELF)

        # normalization
        old_password = input.old_password.strip()
        new_password = input.new_password.strip()

        ensure_password_is_strong(new_password)

        user = await uow.auth_read_repository.get_user_by_id(actor.id)
        if not user:
            raise InvariantViolationError(
                "Actor doesn't exist"
            )

        if not password_hasher.verify(old_password, user.password_hash):
            raise PasswordMissmatchError()

        if password_hasher.verify(new_password, user.password_hash):
            raise PasswordReuseError()

        new_password_hash = password_hasher.hash(new_password)

        await uow.me_update_repository.update_password_by_id(
            user_id=actor.id,
            password_hash=new_password_hash
        )

    async def get_me_profile(
        self,
        actor: Actor,
        uow: MeUoWPort
    ) -> UserProfileEntity:
        ensure_has_permission(actor, Permission.READ_SELF)

        return await uow.me_read_repository.get_profile_by_id(actor.id)

    async def update_me_profile(
        self,
        input: UpdateMeProfileInputDTO,
        actor: Actor,
        uow: MeUoWPort
    ) -> None:
        ensure_has_permission(actor, Permission.UPDATE_SELF)

        # normalization
        first_name = input.first_name.strip()
        last_name = input.last_name.strip()

        ensure_first_name_is_valid(first_name)
        ensure_last_name_is_valid(last_name)

        profile = UserProfileEntity(
            first_name=first_name,
            last_name=last_name
        )

        await uow.me_update_repository.update_profile_by_id(
            user_id=actor.id,
            profile=profile
        )

    async def delete_me(
        self,
        actor: Actor,
        refresh_uow: AuthUoWPort,
        uow: MeUoWPort,
        password_hasher: PasswordHasherPort
    ) -> None:
        if Permission.NO_SELF_DELETE in actor.permissions:
            raise AdminCantSelfDeleteError()

        ensure_has_permission(actor, Permission.DELETE_SELF)

        random_password = secrets.token_urlsafe(128)
        hashed_password = password_hasher.hash(random_password)

        await uow.me_delete_repository.soft_delete_user(
            user_id=actor.id,
            new_password_hash=hashed_password
        )

        await refresh_uow.auth_update_repository.revoke_all_refresh_token(
            user_id=actor.id
        )
