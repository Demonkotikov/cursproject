from sqlalchemy.orm import Session
from app.models.participation import Participation
from app.models.profile import Profile
from app.models.olympiad import Olympiad
from app.shemas.participation_schema import ParticipationCreate

def register_student(db: Session, data: ParticipationCreate):
    # 1. Проверяем, существует ли студент
    student = db.query(Profile).filter(Profile.id == data.student_id).first()
    if not student:
        raise ValueError("Студент с таким ID не найден")

    # 2. Проверяем, существует ли олимпиада
    olympiad = db.query(Olympiad).filter(Olympiad.id == data.olympiad_id).first()
    if not olympiad:
        raise ValueError("Олимпиада с таким ID не найдена")

    # 3. Проверяем, не записан ли уже
    existing = db.query(Participation).filter(
        Participation.student_id == data.student_id,
        Participation.olympiad_id == data.olympiad_id
    ).first()
    if existing:
        raise ValueError("Студент уже записан на эту олимпиаду")

    # 4. Создаём запись
    db_participation = Participation(
        student_id=data.student_id,
        olympiad_id=data.olympiad_id,
        status="registered"
    )
    db.add(db_participation)
    db.commit()
    db.refresh(db_participation)
    return db_participation

def get_participations(db: Session):
    return db.query(Participation).all()

def delete_participation(db: Session, participation_id: int):
    participation = db.query(Participation).filter(
        Participation.id == participation_id
    ).first()
    if participation:
        db.delete(participation)
        db.commit()
    return participation