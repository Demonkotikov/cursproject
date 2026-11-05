from sqlalchemy import Column, Integer, String, Date, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.db.database import Base

class Olympiad(Base):
    __tablename__ = "olympiads"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)  # Положение об олимпиаде
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    
    # Ответственный преподаватель (ссылка на профиль)
    responsible_teacher_id = Column(Integer, ForeignKey("profiles.id"), nullable=True)
    teacher = relationship("Profile")

    # Связь с участием
    participations = relationship("Participation", back_populates="olympiad")