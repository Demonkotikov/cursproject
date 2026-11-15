from pydantic import BaseModel, ConfigDict, Field, model_validator
from datetime import date
from typing import Optional


class OlympiadBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    start_date: date
    end_date: date
    responsible_teacher_id: Optional[int] = None


class OlympiadCreate(OlympiadBase):
    @model_validator(mode="after")
    def check_dates(self):
        if self.start_date > self.end_date:
            raise ValueError("Дата начала не может быть позже даты окончания")
        return self


class OlympiadUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    responsible_teacher_id: Optional[int] = None


class OlympiadResponse(OlympiadBase):
    id: int
    model_config = ConfigDict(from_attributes=True)