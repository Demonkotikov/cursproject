from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from app.core.config import settings
from app.db.session import get_db
from app.models.profile import Profile

# Схема OAuth2 (указывает Swagger, куда отправлять логин/пароль)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> Profile:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Не удалось проверить учётные данные",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # Расшифровываем токен
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")  # "sub" — это email пользователя
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    # Ищем пользователя в БД по email
    user = db.query(Profile).filter(Profile.email == email).first()
    if user is None:
        raise credentials_exception
    return user

# Зависимость для проверки роли "admin"
def get_current_admin(current_user: Profile = Depends(get_current_user)) -> Profile:
    if current_user.role.name != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Недостаточно прав. Требуется роль 'admin'."
        )
    return current_user