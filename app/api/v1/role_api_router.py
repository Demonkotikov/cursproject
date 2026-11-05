from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.controllers import role_controller
from app.shemas.role_shema import RoleCreate, RoleResponse

router = APIRouter(prefix="/roles", tags=["Роли"])

@router.get("/", response_model=list[RoleResponse])
def read_roles(db: Session = Depends(get_db)):
    return role_controller.get_roles(db)

@router.post("/", response_model=RoleResponse)
def create_role(role: RoleCreate, db: Session = Depends(get_db)):
    return role_controller.create_role(db, role)