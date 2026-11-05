from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.controllers import profile_controller
from app.shemas.profile_schema import ProfileCreate, ProfileResponse

router = APIRouter(prefix="/profiles", tags=["Профили"])

@router.get("/", response_model=list[ProfileResponse])
def read_profiles(db: Session = Depends(get_db)):
    return profile_controller.get_profiles(db)

@router.post("/", response_model=ProfileResponse)
def create_profile(profile: ProfileCreate, db: Session = Depends(get_db)):
    return profile_controller.create_profile(db, profile)