from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base

class TaskBucket(Base):
    __tablename__ = "task_buckets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    order = Column(Integer, nullable=False)

    phase_id = Column(Integer, ForeignKey("project_phases.id"), nullable=False)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)

    tasks = relationship("Task", back_populates="bucket", cascade="all, delete")
    phase = relationship("ProjectPhase", back_populates="task_buckets")
    project = relationship("Project", back_populates="task_buckets")
