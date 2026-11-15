from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.controllers import profile_controller
from app.shemas.profile_schema import (
    ProfileAdminCreate,
    ProfileResponse,
    ProfileUpdate,
)
from app.core.dependencies import (
    get_current_active_user,
    get_current_admin,
    require_role,
)
from app.models.profile import Profile

router = APIRouter(prefix="/profiles", tags=["Профили"])


@router.get("/me", response_model=ProfileResponse, summary="Мой профиль")
def read_me(current_user: Profile = Depends(get_current_active_user)):
    return current_user


@router.patch("/me", response_model=ProfileResponse, summary="Обновить мой профиль")
def update_me(
    payload: ProfileUpdate,
    db: Session = Depends(get_db),
    current_user: Profile = Depends(get_current_active_user),
):
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(current_user, key, value)
    db.commit()
    db.refresh(current_user)
    return current_user


@router.get("/", response_model=list[ProfileResponse],
            summary="Список профилей (админ/преподаватель)")
def read_profiles(
    db: Session = Depends(get_db),
    _: Profile = Depends(require_role("admin", "teacher")),
):
    return profile_controller.get_profiles(db)


@router.get("/{profile_id}", response_model=ProfileResponse,
            summary="Профиль по id (админ/преподаватель)")
def read_profile(
    profile_id: int,
    db: Session = Depends(get_db),
    _: Profile = Depends(require_role("admin", "teacher")),
):
    profile = profile_controller.get_profile_by_id(db, profile_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Профиль не найден")
    return profile


@router.post("/", response_model=ProfileResponse, status_code=status.HTTP_201_CREATED,
             summary="Создать профиль (только админ)")
def create_profile(
    payload: ProfileAdminCreate,
    db: Session = Depends(get_db),
    _: Profile = Depends(get_current_admin),
):
    try:
        return profile_controller.create_profile_admin(db, payload)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.patch("/{profile_id}", response_model=ProfileResponse,
              summary="Обновить профиль (только админ)")
def update_profile(
    profile_id: int,
    update_data: dict,
    db: Session = Depends(get_db),
    _: Profile = Depends(get_current_admin),
):
    try:
        profile = profile_controller.update_profile(db, profile_id, update_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    if not profile:
        raise HTTPException(status_code=404, detail="Профиль не найден")
    return profile


@router.delete("/{profile_id}", status_code=status.HTTP_204_NO_CONTENT,
               summary="Удалить профиль (только админ)")
def delete_profile(
    profile_id: int,
    db: Session = Depends(get_db),
    current_admin: Profile = Depends(get_current_admin),
):
    if profile_id == current_admin.id:
        raise HTTPException(status_code=400, detail="Нельзя удалить собственный профиль")
    try:
        profile = profile_controller.delete_profile(db, profile_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    if not profile:
        raise HTTPException(status_code=404, detail="Профиль не найден")
    return None