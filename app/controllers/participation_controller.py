from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.controllers import participation_controller
from app.shemas.participation_schema import (
    ParticipationCreate,
    ParticipationResponse,
)
from app.core.dependencies import get_current_active_user, require_role
from app.models.profile import Profile

router = APIRouter(prefix="/participations", tags=["Участие в олимпиадах"])


@router.get("/me", response_model=list[ParticipationResponse],
            summary="Мои участия")
def my_participations(
    db: Session = Depends(get_db),
    current_user: Profile = Depends(get_current_active_user),
):
    return participation_controller.get_my_participations(db, current_user.id)


@router.get("/", response_model=list[ParticipationResponse],
            summary="Все участия (админ/преподаватель)")
def read_participations(
    db: Session = Depends(get_db),
    _: Profile = Depends(require_role("admin", "teacher")),
):
    return participation_controller.get_participations(db)


@router.post("/", response_model=ParticipationResponse,
             status_code=status.HTTP_201_CREATED,
             summary="Записаться на олимпиаду (только студент)")
def register_student(
    payload: ParticipationCreate,
    db: Session = Depends(get_db),
    current_user: Profile = Depends(require_role("student")),
):
    try:
        return participation_controller.register_student(
            db,
            student_id=current_user.id,
            olympiad_id=payload.olympiad_id,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{participation_id}", status_code=status.HTTP_204_NO_CONTENT,
               summary="Удалить участие (только админ)")
def delete_participation(
    participation_id: int,
    db: Session = Depends(get_db),
    _: Profile = Depends(require_role("admin")),
):
    participation = participation_controller.delete_participation(
        db, participation_id
    )
    if not participation:
        raise HTTPException(status_code=404, detail="Запись об участии не найдена")
    return None