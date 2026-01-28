from pydantic import BaseModel, EmailStr

from app.domain.auth.role import Role


class LoginInputDTO(BaseModel):
    email: EmailStr
    password: str


class TokenOutputDTO(BaseModel):
    access_token: str
    token_type: str


class GetMeOutputDTO(BaseModel):
    email: EmailStr
    roles: set[Role]
