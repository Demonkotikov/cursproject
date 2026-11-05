from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.controllers import olympiad_controller
from app.shemas.olympiad_schema import OlympiadCreate, OlympiadResponse

router = APIRouter(prefix="/olympiads", tags=["Олимпиады"])

@router.get("/", response_model=list[OlympiadResponse])
def read_olympiads(db: Session = Depends(get_db)):
    return olympiad_controller.get_olympiads(db)

@router.post("/", response_model=OlympiadResponse)
def create_olympiad(olympiad: OlympiadCreate, db: Session = Depends(get_db)):
    return olympiad_controller.create_olympiad(db, olympiad)