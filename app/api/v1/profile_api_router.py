from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.controllers import profile_controller
from app.shemas.profile_schema import ProfileCreate, ProfileResponse
from fastapi import HTTPException
from app.models.profile import Profile

router = APIRouter(prefix="/profiles", tags=["Профили"])

@router.get("/", response_model=list[ProfileResponse],summary="Получить список всех профилей")
def read_profiles(db: Session = Depends(get_db)):
    return profile_controller.get_profiles(db)

@router.post("/", response_model=ProfileResponse,summary="создание профиля")
def create_profile(profile: ProfileCreate, db: Session = Depends(get_db)):
    return profile_controller.create_profile(db, profile)

@router.get("/{profile_id}", response_model=ProfileResponse,summary="список профилей по id")
def read_profile(profile_id: int, db: Session = Depends(get_db)):
    profile = db.query(Profile).filter(Profile.id == profile_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Профиль не найден")
    return profile

from fastapi import HTTPException

@router.delete("/{profile_id}", status_code=204,summary="удаление профиля")
def delete_profile(profile_id: int, db: Session = Depends(get_db)):
    profile = profile_controller.delete_profile(db, profile_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Профиль не найден")
    return None

@router.patch("/{profile_id}", response_model=ProfileResponse,summary="обновление профилей")
def update_profile(
    profile_id: int, 
    update_data: dict, 
    db: Session = Depends(get_db)
):
    profile = profile_controller.update_profile(db, profile_id, update_data)
    if not profile:
        raise HTTPException(status_code=404, detail="Профиль не найден")
    return profile