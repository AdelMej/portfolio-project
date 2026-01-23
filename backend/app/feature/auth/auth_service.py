from app.feature.auth.auth_dto import (
    LoginInputDTO,
    TokenOutputDTO
)
from app.domain.auth.auth_exceptions import (
    InvalidEmailError,
    InvalidPasswordError
)
from app.shared.security.jwt_port import JwtPort
from app.shared.security.password_hasher_port import PasswordHasherPort


class AuthService:
    def __init__(self, uow) -> None:
        self._uow = uow

    async def login(
        self,
        input: LoginInputDTO,
        jwt: JwtPort,
        password_hasher: PasswordHasherPort
    ) -> TokenOutputDTO:
        # normalization
        email = input.email.strip().lower()
        password = input.password.strip()

        async with self._uow as uow:
            if not await uow.auth_read.exist_email(email):
                raise InvalidEmailError()

            user = await uow.auth_read.get_user_by_email(email)

            if not password_hasher.verify(password, user.password_hash):
                raise InvalidPasswordError()

            refresh_token = await uow.auth_update.rotate_refresh_token(user.id)

            refresh_jwt = jwt.issue_refresh_token(
                user_id=user.id,
                token_id=refresh_token.id
            )
            return TokenOutputDTO(
                access_token=jwt.issue_access_token(
                    user_id=user.id
                ),
                refresh_token=refresh_jwt
            )
