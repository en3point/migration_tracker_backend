from sqlalchemy import Column, Integer, String, Date, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.db.database import Base

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    subsystem_id = Column(Integer, ForeignKey("subsystems.id"), nullable=True)
    team_id = Column(Integer, ForeignKey("teams.id"), nullable=True)
    task_bucket_id = Column(Integer, ForeignKey("task_buckets.id"), nullable=False)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)

    vendor_system = Column(String, nullable=False)
    subject = Column(String, nullable=False)
    description = Column(String, nullable=False)
    detailed_description = Column(String)
    start_date = Column(Date)
    end_date = Column(Date)
    order = Column(Integer, nullable=False)

    bucket = relationship("TaskBucket", back_populates="tasks")
    project = relationship("Project", back_populates="tasks")
