from pydantic import BaseModel
from typing import Optional

class ParticipationCreate(BaseModel):
    student_id: int
    olympiad_id: int

class ParticipationResponse(ParticipationCreate):
    id: int
    status: str
    result_place: Optional[int] = None
    score: Optional[int] = None

    class Config:
        from_attributes = True