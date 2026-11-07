from sqlalchemy.orm import Session
from app.models.profile import Profile
from app.models.role import Role
from app.shemas.profile_schema import ProfileCreate
from app.core.security import get_password_hash

def create_profile(db: Session, profile_data: ProfileCreate):
    student_role = db.query(Role).filter(Role.name == "student").first()
    if not student_role:
        raise ValueError("Роль 'student' не найдена в БД")
    
    db_profile = Profile(
        email=profile_data.email,
        hashed_password=get_password_hash(profile_data.password),
        last_name=profile_data.last_name,
        first_name=profile_data.first_name,
        middle_name=profile_data.middle_name,
        role_id=student_role.id,
        is_active=True,
    )
    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)
    return db_profile

def get_profiles(db: Session):
    return db.query(Profile).all()

def delete_profile(db: Session, profile_id: int):
    profile = db.query(Profile).filter(Profile.id == profile_id).first()
    if profile:
        db.delete(profile)
        db.commit()
    return profile

def update_profile(db: Session, profile_id: int, update_data: dict):
    profile = db.query(Profile).filter(Profile.id == profile_id).first()
    if profile:
        for key, value in update_data.items():
            setattr(profile, key, value)
        db.commit()
        db.refresh(profile)
    return profile