from pydantic import BaseModel, EmailStr
from typing import Optional
from app.shemas.role_shema import RoleResponse

class ProfileCreate(BaseModel):
    email: EmailStr
    password: str
    last_name: str
    first_name: str
    middle_name: Optional[str] = None

class ProfileResponse(BaseModel):
    id: int
    email: EmailStr
    last_name: str
    first_name: str
    middle_name: Optional[str] = None
    is_active: bool
    role: RoleResponse

    class Config:
        from_attributes = True