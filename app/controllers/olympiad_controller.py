from sqlalchemy.orm import Session
from typing import Optional
from app.models.olympiad import Olympiad
from app.shemas.olympiad_schema import OlympiadCreate

def create_olympiad(db: Session, olympiad: OlympiadCreate):
    db_olympiad = Olympiad(**olympiad.dict())
    db.add(db_olympiad)
    db.commit()
    db.refresh(db_olympiad)
    return db_olympiad

def get_olympiads(db: Session, year: Optional[int] = None):
    query = db.query(Olympiad)
    if year:
        # Фильтр: олимпиады, которые начались в указанном году
        query = query.filter(Olympiad.start_date >= f"{year}-01-01")
        query = query.filter(Olympiad.start_date <= f"{year}-12-31")
    return query.all()

def get_olympiad_by_id(db: Session, olympiad_id: int):
    return db.query(Olympiad).filter(Olympiad.id == olympiad_id).first()

def delete_olympiad(db: Session, olympiad_id: int):
    olympiad = db.query(Olympiad).filter(Olympiad.id == olympiad_id).first()
    if olympiad:
        db.delete(olympiad)
        db.commit()
    return olympiad

def update_olympiad(db: Session, olympiad_id: int, update_data: dict):
    olympiad = db.query(Olympiad).filter(Olympiad.id == olympiad_id).first()
    if olympiad:
        for key, value in update_data.items():
            setattr(olympiad, key, value)
        db.commit()
        db.refresh(olympiad)
    return olympiad