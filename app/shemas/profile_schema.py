from pydantic import BaseModel, EmailStr
from app.shemas.role_shema import RoleResponse

class ProfileCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    role_id: int

class ProfileResponse(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    is_active: bool
    role: RoleResponse

    class Config:
        from_attributes = True