from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.controllers import role_controller
from app.shemas.role_shema import RoleCreate, RoleResponse
from app.core.dependencies import get_current_admin
from app.models.profile import Profile

router = APIRouter(prefix="/roles", tags=["Роли"])


@router.get("/", response_model=list[RoleResponse], summary="Список ролей")
def read_roles(db: Session = Depends(get_db)):
    return role_controller.get_roles(db)


@router.post("/", response_model=RoleResponse, status_code=status.HTTP_201_CREATED,
             summary="Создать роль (только админ)")
def create_role(
    role: RoleCreate,
    db: Session = Depends(get_db),
    _: Profile = Depends(get_current_admin),
):
    return role_controller.create_role(db, role)


@router.patch("/{role_id}", response_model=RoleResponse,
              summary="Обновить роль (только админ)")
def update_role(
    role_id: int,
    update_data: dict,
    db: Session = Depends(get_db),
    _: Profile = Depends(get_current_admin),
):
    role = role_controller.update_role(db, role_id, update_data)
    if not role:
        raise HTTPException(status_code=404, detail="Роль не найдена")
    return role


@router.delete("/{role_id}", status_code=status.HTTP_204_NO_CONTENT,
               summary="Удалить роль (только админ)")
def delete_role(
    role_id: int,
    db: Session = Depends(get_db),
    _: Profile = Depends(get_current_admin),
):
    try:
        role = role_controller.delete_role(db, role_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    if not role:
        raise HTTPException(status_code=404, detail="Роль не найдена")
    return None