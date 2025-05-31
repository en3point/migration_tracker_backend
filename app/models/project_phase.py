from sqlalchemy import Column, Integer, String, Date
from app.db.database import Base

class ProjectPhase(Base):
    __tablename__ = "project_phases"
    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, index=True)
    label = Column(String)