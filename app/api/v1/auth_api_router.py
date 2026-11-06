from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.security import verify_password, create_access_token
from app.models.profile import Profile
from app.shemas.auth_schema import Token

router = APIRouter(prefix="/auth", tags=["Аутентификация"])

@router.post("/login", response_model=Token, summary="Вход в систему")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """Принимает email и пароль, возвращает JWT-токен."""
    # Ищем пользователя по email
    user = db.query(Profile).filter(Profile.email == form_data.username).first()
    
    # Проверяем пароль
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный email или пароль",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Создаём токен (в поле "sub" кладём email пользователя)
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}