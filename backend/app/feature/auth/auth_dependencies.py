from functools import lru_cache
from fastapi.security import OAuth2PasswordBearer

from app.feature.auth.auth_service import AuthService


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


@lru_cache()
def get_auth_service() -> AuthService:
    return AuthService()
