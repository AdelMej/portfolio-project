import pytest
from uuid import uuid4

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

from app.domain.user.user_entity import User
from app.feature.auth.auth_service import AuthService
from app.feature.auth.auth_dto import LoginInputDTO


@pytest.mark.anyio
async def test_login_success():
    storage = InMemoryAuthStorage()

    user_id = uuid4()
    user = User(
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

    result = await service.login(
        LoginInputDTO(email="test@test.com", password="secret"),
        jwt=InMemoryJwt(),
        password_hasher=InMemoryPasswordHasher(),
    )

    assert result.access_token.startswith("access:")
    assert result.refresh_token.startswith("refresh:")
    assert len(storage.refresh_tokens) == 1
