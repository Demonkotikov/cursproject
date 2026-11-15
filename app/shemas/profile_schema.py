from pydantic import BaseModel, ConfigDict, EmailStr, Field
from typing import Optional
from app.shemas.role_shema import RoleResponse


class ProfileBase(BaseModel):
    email: EmailStr
    last_name: str = Field(..., min_length=1, max_length=100)
    first_name: str = Field(..., min_length=1, max_length=100)
    middle_name: Optional[str] = Field(None, max_length=100)


class ProfileCreate(ProfileBase):
    """Публичная регистрация студента (роль student ставится автоматически)."""
    password: str = Field(..., min_length=6)


class ProfileAdminCreate(ProfileBase):
    """Создание профиля админом — с явной ролью."""
    password: str = Field(..., min_length=6)
    role_id: int


class ProfileUpdate(BaseModel):
    last_name: Optional[str] = Field(None, min_length=1, max_length=100)
    first_name: Optional[str] = Field(None, min_length=1, max_length=100)
    middle_name: Optional[str] = Field(None, max_length=100)


class ProfileResponse(ProfileBase):
    id: int
    is_active: bool
    role_id: int
    role: RoleResponse

    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"