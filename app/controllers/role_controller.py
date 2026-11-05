from sqlalchemy.orm import Session
from app.models.role import Role
from app.shemas.role_shema import RoleCreate

def create_role(db: Session, role_data: RoleCreate):
    db_role = Role(name=role_data.name)
    db.add(db_role)
    db.commit()
    db.refresh(db_role)
    return db_role

def get_roles(db: Session):
    return db.query(Role).all()