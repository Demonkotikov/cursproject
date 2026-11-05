from pydantic import BaseModel
from datetime import date
from typing import Optional

class OlympiadCreate(BaseModel):
    title: str
    description: Optional[str] = None
    start_date: date
    end_date: date
    responsible_teacher_id: Optional[int] = None

class OlympiadResponse(OlympiadCreate):
    id: int

    class Config:
        from_attributes = True