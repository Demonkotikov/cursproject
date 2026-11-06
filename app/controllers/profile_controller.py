from sqlalchemy.orm import Session
from app.models.profile import Profile
from app.shemas.profile_schema import ProfileCreate

def create_profile(db: Session, profile_data: ProfileCreate):
    db_profile = Profile(
        email=profile_data.email,
        hashed_password=profile_data.password,  # В реальности нужно хэшировать!
        full_name=profile_data.full_name,
        role_id=profile_data.role_id
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