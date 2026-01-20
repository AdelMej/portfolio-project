from pydantic import BaseModel

class SessionInputDTO (BaseModel):
    email: str
    firstName: str
