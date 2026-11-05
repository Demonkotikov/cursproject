from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.controllers import participation_controller
from app.shemas.participation_schema import ParticipationCreate, ParticipationResponse

router = APIRouter(prefix="/participations", tags=["Участие в олимпиадах"])

@router.get("/", response_model=list[ParticipationResponse])
def read_participations(db: Session = Depends(get_db)):
    return participation_controller.get_participations(db)

@router.post("/", response_model=ParticipationResponse)
def register_student(participation: ParticipationCreate, db: Session = Depends(get_db)):
    return participation_controller.register_student(db, participation)