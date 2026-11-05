from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base

class Participation(Base):
    __tablename__ = "participations"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("profiles.id"), nullable=False)
    olympiad_id = Column(Integer, ForeignKey("olympiads.id"), nullable=False)
    
    # Статус: registered, completed, winner
    status = Column(String(50), default="registered")
    result_place = Column(Integer, nullable=True)  # 1, 2, 3 место
    score = Column(Integer, nullable=True)         # Баллы

    student = relationship("Profile")
    olympiad = relationship("Olympiad", back_populates="participations")