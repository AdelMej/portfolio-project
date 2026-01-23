from datetime import timedelta
import pytest
from uuid import uuid4

from app.domain.auth.refresh_token_entity import RefreshTokenEntity
from app.infrastructure.persistence.in_memory.storage import (
    InMemoryAuthStorage,
)
from app.infrastructure.persistence.in_memory.auth.auth_uow import (
    InMemoryAuthUoW
)
from app.infrastructure.security.in_memory.jwt import InMemoryJwt
from app.infrastructure.security.in_memory.password_hasher import (
    InMemoryPasswordHasher
)

from app.domain.user.user_entity import UserEntity
from app.feature.auth.auth_service import AuthService
from app.feature.auth.auth_dto import LoginInputDTO
from app.infrastructure.security.in_memory.refresh_token_generator import (
    InMemoryRefreshTokenGenerator
)
from app.infrastructure.security.in_memory.token_hasher import (
    InMemoryTokenHasher
)
from app.domain.auth.auth_exceptions import (
    InvalidEmailError,
    InvalidPasswordError,
    UserDisabledError
)
from app.shared.utils.time import utcnow


@pytest.mark.anyio
async def test_login_success():
    storage = InMemoryAuthStorage()

    user_id = uuid4()
    user = UserEntity(
        id=user_id,
        email="test@test.com",
        password_hash="secret",
        disabled_at=None,
        disabled_reason=None
    )

    storage.users[user_id] = user
    storage.users_by_email[user.email] = user_id

    uow = InMemoryAuthUoW(storage)
    service = AuthService(uow)

    access, refresh = await service.login(
        input=LoginInputDTO(
            email="test@test.com",
            password="secret"
        ),
        existing_refresh=None,
        refresh_token_ttl=3600,
        token_hasher=InMemoryTokenHasher(),
        refresh_token_generator=InMemoryRefreshTokenGenerator(),
        jwt=InMemoryJwt(),
        password_hasher=InMemoryPasswordHasher(),
    )

    assert access.startswith("access:")
    assert refresh is not None
    assert len(storage.refresh_tokens) == 1


@pytest.mark.anyio
async def test_login_invalid_email():
    storage = InMemoryAuthStorage()
    service = AuthService(InMemoryAuthUoW(storage))

    with pytest.raises(InvalidEmailError):
        await service.login(
            LoginInputDTO(email="nope@test.com", password="secret"),
            existing_refresh=None,
            refresh_token_ttl=3600,
            jwt=InMemoryJwt(),
            password_hasher=InMemoryPasswordHasher(),
            token_hasher=InMemoryTokenHasher(),
            refresh_token_generator=InMemoryRefreshTokenGenerator(),
        )


@pytest.mark.anyio
async def test_login_invalid_password():
    storage = InMemoryAuthStorage()
    user_id = uuid4()

    storage.users[user_id] = UserEntity(
        id=user_id,
        email="test@test.com",
        password_hash="correct",
        disabled_at=None,
        disabled_reason=None,
    )
    storage.users_by_email["test@test.com"] = user_id

    service = AuthService(InMemoryAuthUoW(storage))

    with pytest.raises(InvalidPasswordError):
        await service.login(
            LoginInputDTO(email="test@test.com", password="wrong"),
            existing_refresh=None,
            refresh_token_ttl=3600,
            jwt=InMemoryJwt(),
            password_hasher=InMemoryPasswordHasher(),
            token_hasher=InMemoryTokenHasher(),
            refresh_token_generator=InMemoryRefreshTokenGenerator(),
        )


@pytest.mark.anyio
async def test_login_revokes_existing_refresh_token():
    storage = InMemoryAuthStorage()
    user_id = uuid4()

    user = UserEntity(
        id=user_id,
        email="test@test.com",
        password_hash="secret",
        disabled_at=None,
        disabled_reason=None,
    )

    storage.users[user_id] = user
    storage.users_by_email[user.email] = user_id

    old_token_hash = "old_hash"
    storage.refresh_tokens[old_token_hash] = RefreshTokenEntity(
        user_id=user_id,
        token_hash=old_token_hash,
        created_at=utcnow(),
        expires_at=utcnow() + timedelta(hours=1),
        revoked_at=None,
    )

    service = AuthService(InMemoryAuthUoW(storage))

    _, _ = await service.login(
        LoginInputDTO(email="test@test.com", password="secret"),
        existing_refresh=old_token_hash,
        refresh_token_ttl=3600,
        jwt=InMemoryJwt(),
        password_hasher=InMemoryPasswordHasher(),
        token_hasher=InMemoryTokenHasher(),
        refresh_token_generator=InMemoryRefreshTokenGenerator(),
    )

    assert storage.refresh_tokens[old_token_hash].revoked_at is not None
    assert len(storage.refresh_tokens) == 2


@pytest.mark.anyio
async def test_login_ignores_expired_refresh_token():
    storage = InMemoryAuthStorage()
    user_id = uuid4()

    storage.users[user_id] = UserEntity(
        id=user_id,
        email="test@test.com",
        password_hash="secret",
        disabled_at=None,
        disabled_reason=None,
    )
    storage.users_by_email["test@test.com"] = user_id

    token_hash = "old_hash"
    storage.refresh_tokens[token_hash] = RefreshTokenEntity(
        user_id=user_id,
        token_hash=token_hash,
        created_at=utcnow() - timedelta(days=1),
        expires_at=utcnow() - timedelta(seconds=10),
        revoked_at=None,
    )

    service = AuthService(InMemoryAuthUoW(storage))

    access, refresh = await service.login(
        input=LoginInputDTO(email="test@test.com", password="secret"),
        existing_refresh=token_hash,
        refresh_token_ttl=3600,
        jwt=InMemoryJwt(),
        password_hasher=InMemoryPasswordHasher(),
        token_hasher=InMemoryTokenHasher(),
        refresh_token_generator=InMemoryRefreshTokenGenerator(),
    )

    new_hash = InMemoryTokenHasher().hash(refresh)

    assert access.startswith("access:")
    assert new_hash != token_hash
    assert new_hash in storage.refresh_tokens
    assert token_hash in storage.refresh_tokens
    assert storage.refresh_tokens[token_hash].revoked_at is not None


@pytest.mark.anyio
async def test_login_disabled_user():
    storage = InMemoryAuthStorage()
    user_id = uuid4()

    storage.users[user_id] = UserEntity(
        id=user_id,
        email="test@test.com",
        password_hash="secret",
        disabled_at=utcnow(),
        disabled_reason="admin ban",
    )
    storage.users_by_email["test@test.com"] = user_id

    service = AuthService(InMemoryAuthUoW(storage))

    with pytest.raises(UserDisabledError):
        await service.login(
            LoginInputDTO(email="test@test.com", password="secret"),
            existing_refresh=None,
            refresh_token_ttl=3600,
            jwt=InMemoryJwt(),
            password_hasher=InMemoryPasswordHasher(),
            token_hasher=InMemoryTokenHasher(),
            refresh_token_generator=InMemoryRefreshTokenGenerator(),
        )

    assert len(storage.refresh_tokens) == 0


@pytest.mark.anyio
async def test_login_rotates_existing_refresh_token():
    storage = InMemoryAuthStorage()
    user_id = uuid4()

    storage.users[user_id] = UserEntity(
        id=user_id,
        email="test@test.com",
        password_hash="secret",
        disabled_at=None,
        disabled_reason=None,
    )
    storage.users_by_email["test@test.com"] = user_id

    token_hasher = InMemoryTokenHasher()

    old_refresh_plain = "old_refresh"
    old_refresh_hash = token_hasher.hash(old_refresh_plain)

    storage.refresh_tokens[old_refresh_hash] = RefreshTokenEntity(
        user_id=user_id,
        token_hash=old_refresh_hash,
        created_at=utcnow() - timedelta(hours=1),
        expires_at=utcnow() + timedelta(hours=1),
        revoked_at=None,
    )

    service = AuthService(InMemoryAuthUoW(storage))

    access, new_refresh = await service.login(
        input=LoginInputDTO(email="test@test.com", password="secret"),
        existing_refresh=old_refresh_plain,
        refresh_token_ttl=3600,
        jwt=InMemoryJwt(),
        password_hasher=InMemoryPasswordHasher(),
        token_hasher=InMemoryTokenHasher(),
        refresh_token_generator=InMemoryRefreshTokenGenerator(),
    )

    # old token revoked
    assert storage.refresh_tokens[old_refresh_hash].revoked_at is not None

    # new token created
    assert len(storage.refresh_tokens) == 2
    assert new_refresh != old_refresh_plain
    assert access.startswith("access:")


@pytest.mark.anyio
async def test_login_fails_for_disabled_user():
    storage = InMemoryAuthStorage()
    user_id = uuid4()

    storage.users[user_id] = UserEntity(
        id=user_id,
        email="test@test.com",
        password_hash="secret",
        disabled_at=utcnow(),
        disabled_reason="banned",
    )
    storage.users_by_email["test@test.com"] = user_id

    service = AuthService(InMemoryAuthUoW(storage))

    with pytest.raises(UserDisabledError):
        await service.login(
            input=LoginInputDTO(email="test@test.com", password="secret"),
            existing_refresh=None,
            refresh_token_ttl=3600,
            jwt=InMemoryJwt(),
            password_hasher=InMemoryPasswordHasher(),
            token_hasher=InMemoryTokenHasher(),
            refresh_token_generator=InMemoryRefreshTokenGenerator(),
        )
