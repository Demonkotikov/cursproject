from pydantic import BaseModel, ConfigDict
from typing import Optional


class ParticipationCreate(BaseModel):
    olympiad_id: int


class ParticipationResponse(BaseModel):
    id: int
    student_id: int
    olympiad_id: int
    status: str
    result_place: Optional[int] = None
    score: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)