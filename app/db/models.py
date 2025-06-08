# models.py
from sqlalchemy import Column, Integer, String, Date, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from app.db.database import Base

class Team(Base):
    __tablename__ = "teams"
    __table_args__ = {'extend_existing': True}  # ✅ Prevent redefinition error
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    email_to = Column(String)
    email_cc = Column(String)
    tasks = relationship("Task", back_populates="team")

class Subsystem(Base):
    __tablename__ = "subsystems"
    __table_args__ = {'extend_existing': True}  # ✅ Prevent redefinition error
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    tasks = relationship("Task", back_populates="subsystem")

class ProjectPhase(Base):
    __tablename__ = "project_phases"
    __table_args__ = {'extend_existing': True}  # ✅ Prevent redefinition error
    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, unique=True)
    label = Column(String)

class Task(Base):
    __tablename__ = "tasks"
    __table_args__ = {'extend_existing': True}  # ✅ Prevent redefinition error

    id = Column(Integer, primary_key=True, index=True)
    task_bucket_id = Column(Integer, ForeignKey("task_buckets.id"), nullable=False)
    subsystem_id = Column(Integer, ForeignKey("subsystems.id"))
    team_id = Column(Integer, ForeignKey("teams.id"))
    vendor_system = Column(String)
    subject = Column(String, nullable=False)
    description = Column(String, nullable=False)
    detailed_description = Column(String)
    start_date = Column(Date)
    end_date = Column(Date)
    status_by_day = Column(JSON, default={})
    order = Column(Integer, nullable=False)

    task_bucket = relationship("TaskBucket", back_populates="tasks")
    subsystem = relationship("Subsystem")
    team = relationship("Team")
    
class TaskBucket(Base):
    __tablename__ = "task_buckets"
    __table_args__ = {'extend_existing': True}  # ✅ Prevent redefinition error
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    order = Column(Integer, nullable=False)

    tasks = relationship("Task", back_populates="task_bucket", cascade="all, delete")
