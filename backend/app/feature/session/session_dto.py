from datetime import datetime
from pydantic import BaseModel
from uuid import UUID

class GetOutputDto(BaseModel):
    id: UUID
    coach_id: UUID
    title: str
    starts_at: datetime
    ends_at: datetime
    status: str

# Added session coach

class SessionCreateRequest(BaseModel):
    title: str
    starts_at: datetime
    ends_at: datetime

class AttendanceOutputDto(BaseModel):
    user_id: UUID