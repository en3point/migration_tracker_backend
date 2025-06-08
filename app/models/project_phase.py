from sqlalchemy import Column, Integer, String, Date
from app.db.database import Base

class ProjectPhase(Base):
    __tablename__ = "project_phases"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False)
    label = Column(String, nullable=False)

    # Relationships
    task_buckets = relationship("TaskBucket", back_populates="phase", cascade="all, delete")
