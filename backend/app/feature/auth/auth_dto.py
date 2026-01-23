from pydantic import BaseModel, EmailStr


class LoginInputDTO(BaseModel):
    email: EmailStr
    password: str


class TokenOutputDTO(BaseModel):
    access_token: str
    refresh_token: str
