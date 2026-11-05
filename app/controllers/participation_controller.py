from sqlalchemy.orm import Session
from app.models.participation import Participation
from app.shemas.participation_schema import ParticipationCreate

def register_student(db: Session, data: ParticipationCreate):
    # Проверка: не записан ли уже студент
    existing = db.query(Participation).filter(
        Participation.student_id == data.student_id,
        Participation.olympiad_id == data.olympiad_id
    ).first()
    
    if existing:
        return existing # Или можно выбрасывать ошибку, что уже записан

    db_participation = Participation(
        student_id=data.student_id,
        olympiad_id=data.olympiad_id
    )
    db.add(db_participation)
    db.commit()
    db.refresh(db_participation)
    return db_participation

def get_participations(db: Session):
    return db.query(Participation).all()