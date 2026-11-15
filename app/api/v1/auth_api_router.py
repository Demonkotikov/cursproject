from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.core.security import verify_password, create_access_token
from app.models.profile import Profile
from app.shemas.profile_schema import Token, ProfileCreate, ProfileResponse
from app.controllers import profile_controller

router = APIRouter(prefix="/auth", tags=["Аутентификация"])


@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = db.query(Profile).filter(Profile.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный email или пароль",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.is_active:
        raise HTTPException(status_code=403, detail="Пользователь заблокирован")
    token = create_access_token({"sub": user.email, "role": user.role.name})
    return Token(access_token=token)


@router.post("/register", response_model=ProfileResponse,
             status_code=status.HTTP_201_CREATED,
             summary="Публичная регистрация студента")
def register(payload: ProfileCreate, db: Session = Depends(get_db)):
    try:
        return profile_controller.create_student(db, payload)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))