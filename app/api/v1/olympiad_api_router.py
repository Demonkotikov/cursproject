from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from app.db.session import get_db
from app.controllers import olympiad_controller
from app.shemas.olympiad_schema import OlympiadCreate, OlympiadResponse

router = APIRouter(prefix="/olympiads", tags=["Олимпиады"])

# GET /olympiads/ — список всех (с фильтрацией по году)
@router.get("/", response_model=list[OlympiadResponse],summary="Получить список всех олимпиад")
def read_olympiads(
    year: Optional[int] = None,  # ← Фильтр по году (из ТЗ)
    db: Session = Depends(get_db)
):
    return olympiad_controller.get_olympiads(db, year=year)

# GET /olympiads/{id} — одна олимпиада
@router.get("/{olympiad_id}", response_model=OlympiadResponse,summary="Получить олимпиады по id")
def read_olympiad(olympiad_id: int, db: Session = Depends(get_db)):
    olympiad = olympiad_controller.get_olympiad_by_id(db, olympiad_id)
    if not olympiad:
        raise HTTPException(status_code=404, detail="Олимпиада не найдена")
    return olympiad

# POST /olympiads/ — создание (пока без проверки роли, добавим позже)
@router.post("/", response_model=OlympiadResponse, status_code=201,summary="создание олимпиад")
def create_olympiad(olympiad: OlympiadCreate, db: Session = Depends(get_db)):
    return olympiad_controller.create_olympiad(db, olympiad)


@router.delete("/{olympiad_id}", status_code=204,summary="удаление олимпиады")
def delete_olympiad(olympiad_id: int, db: Session = Depends(get_db)):
    olympiad = olympiad_controller.delete_olympiad(db, olympiad_id)
    if not olympiad:
        raise HTTPException(status_code=404, detail="Олимпиада не найдена")
    return None

@router.patch("/{olympiad_id}", response_model=OlympiadResponse,summary="обновление олимпиад")
def update_olympiad(
    olympiad_id: int, 
    update_data: dict, 
    db: Session = Depends(get_db)
):
    olympiad = olympiad_controller.update_olympiad(db, olympiad_id, update_data)
    if not olympiad:
        raise HTTPException(status_code=404, detail="Олимпиада не найдена")
    return olympiad