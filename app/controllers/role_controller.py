from sqlalchemy.orm import Session
from app.models.role import Role
from app.shemas.role_shema import RoleCreate
from app.models.profile import Profile  # ← Импортируем Profile

def create_role(db: Session, role_data: RoleCreate):
    db_role = Role(name=role_data.name)
    db.add(db_role)
    db.commit()
    db.refresh(db_role)
    return db_role

def get_roles(db: Session):
    return db.query(Role).all()

def delete_role(db: Session, role_id: int):
    role = db.query(Role).filter(Role.id == role_id).first()
    if not role:
        return None
    
    # Проверяем, есть ли профили с этой ролью
    profiles_count = db.query(Profile).filter(Profile.role_id == role_id).count()
    if profiles_count > 0:
        raise ValueError(
            f"Нельзя удалить роль '{role.name}': к ней привязано {profiles_count} пользователей. "
            f"Сначала перепривяжите их к другой роли или удалите."
        )
    
    db.delete(role)
    db.commit()
    return role

def update_role(db: Session, role_id: int, update_data: dict):
    role = db.query(Role).filter(Role.id == role_id).first()
    if role:
        for key, value in update_data.items():
            setattr(role, key, value)
        db.commit()
        db.refresh(role)
    return role