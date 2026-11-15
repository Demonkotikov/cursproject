from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional

from app.db.session import get_db
from app.controllers import olympiad_controller
from app.shemas.olympiad_schema import (
    OlympiadCreate,
    OlympiadUpdate,
    OlympiadResponse,
)
from app.core.dependencies import get_current_admin
from app.models.profile import Profile

router = APIRouter(prefix="/olympiads", tags=["Олимпиады"])


@router.get("/", response_model=list[OlympiadResponse],
            summary="Список олимпиад (публично)")
def read_olympiads(
    year: Optional[int] = None,
    db: Session = Depends(get_db),
):
    return olympiad_controller.get_olympiads(db, year=year)


@router.get("/{olympiad_id}", response_model=OlympiadResponse,
            summary="Олимпиада по id (публично)")
def read_olympiad(olympiad_id: int, db: Session = Depends(get_db)):
    olympiad = olympiad_controller.get_olympiad_by_id(db, olympiad_id)
    if not olympiad:
        raise HTTPException(status_code=404, detail="Олимпиада не найдена")
    return olympiad


@router.post("/", response_model=OlympiadResponse, status_code=status.HTTP_201_CREATED,
             summary="Создать олимпиаду (только админ)")
def create_olympiad(
    olympiad: OlympiadCreate,
    db: Session = Depends(get_db),
    _: Profile = Depends(get_current_admin),
):
    try:
        return olympiad_controller.create_olympiad(db, olympiad)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.patch("/{olympiad_id}", response_model=OlympiadResponse,
              summary="Обновить олимпиаду (только админ)")
def update_olympiad(
    olympiad_id: int,
    update_data: OlympiadUpdate,
    db: Session = Depends(get_db),
    _: Profile = Depends(get_current_admin),
):
    olympiad = olympiad_controller.update_olympiad(db, olympiad_id, update_data)
    if not olympiad:
        raise HTTPException(status_code=404, detail="Олимпиада не найдена")
    return olympiad


@router.delete("/{olympiad_id}", status_code=status.HTTP_204_NO_CONTENT,
               summary="Удалить олимпиаду (только админ)")
def delete_olympiad(
    olympiad_id: int,
    db: Session = Depends(get_db),
    _: Profile = Depends(get_current_admin),
):
    olympiad = olympiad_controller.delete_olympiad(db, olympiad_id)
    if not olympiad:
        raise HTTPException(status_code=404, detail="Олимпиада не найдена")
    return None