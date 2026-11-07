from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base

class Profile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    
    # Разделяем ФИО
    last_name = Column(String(100), nullable=False)   # Фамилия
    first_name = Column(String(100), nullable=False)  # Имя
    middle_name = Column(String(100), nullable=True)  # Отчество (может отсутствовать)
    
    is_active = Column(Boolean, default=True)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)
    
    role = relationship("Role", back_populates="profiles")
    participations = relationship("Participation", back_populates="student")