from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.controllers import role_controller
from app.shemas.role_shema import RoleCreate, RoleResponse

router = APIRouter(prefix="/roles", tags=["Роли"])

@router.get("/", response_model=list[RoleResponse],summary="Получить список всех ролей")
def read_roles(db: Session = Depends(get_db)):
    return role_controller.get_roles(db)

from app.core.dependencies import get_current_admin  # <-- Импорт

@router.post("/", response_model=RoleResponse, status_code=201, summary="Создать новую роль")
def create_role(
    role: RoleCreate, 
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_admin)  # <-- Защита
):
    """Создаёт новую роль в системе. Доступно только администратору."""
    return role_controller.create_role(db, role)

from fastapi import HTTPException

@router.delete("/{role_id}", status_code=204,summary="удаление роли")
def delete_role(role_id: int, db: Session = Depends(get_db)):
    role = role_controller.delete_role(db, role_id)
    if not role:
        raise HTTPException(status_code=404, detail="Роль не найдена")
    return None

@router.patch("/{role_id}", response_model=RoleResponse,summary="обновить роль")
def update_role(
    role_id: int, 
    update_data: dict, 
    db: Session = Depends(get_db)
):
    role = role_controller.update_role(db, role_id, update_data)
    if not role:
        raise HTTPException(status_code=404, detail="Роль не найдена")
    return role