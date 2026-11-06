from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.controllers import participation_controller
from app.shemas.participation_schema import ParticipationCreate, ParticipationResponse

router = APIRouter(prefix="/participations", tags=["Участие в олимпиадах"])

@router.get("/", response_model=list[ParticipationResponse],summary="Получить список всех участий")
def read_participations(db: Session = Depends(get_db)):
    return participation_controller.get_participations(db)

@router.post("/", response_model=ParticipationResponse, status_code=201,summary="создание участий")
def register_student(participation: ParticipationCreate, db: Session = Depends(get_db)):
    try:
        return participation_controller.register_student(db, participation)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{participation_id}", status_code=204,summary="удаление участий")
def delete_participation(participation_id: int, db: Session = Depends(get_db)):
    participation = participation_controller.delete_participation(db, participation_id)
    if not participation:
        raise HTTPException(status_code=404, detail="Запись об участии не найдена")
    return None