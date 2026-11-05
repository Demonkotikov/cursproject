from sqlalchemy.orm import Session
from app.models.olympiad import Olympiad
from app.shemas.olympiad_schema import OlympiadCreate

def create_olympiad(db: Session, olympiad: OlympiadCreate):
    db_olympiad = Olympiad(**olympiad.dict())
    db.add(db_olympiad)
    db.commit()
    db.refresh(db_olympiad)
    return db_olympiad

def get_olympiads(db: Session):
    return db.query(Olympiad).all()