# models.py
from sqlalchemy import Column, Integer, String, Date, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from app.db.database import Base

class Team(Base):
    __tablename__ = "teams"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    email_to = Column(String)
    email_cc = Column(String)
    tasks = relationship("Task", back_populates="team")

class Subsystem(Base):
    __tablename__ = "subsystems"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    tasks = relationship("Task", back_populates="subsystem")

class ProjectPhase(Base):
    __tablename__ = "project_phases"
    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, unique=True)
    label = Column(String)

class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    subsystem_id = Column(Integer, ForeignKey("subsystems.id"))
    team_id = Column(Integer, ForeignKey("teams.id"), nullable=True)
    vendor_system = Column(String, nullable=True)
    subject = Column(String)
    description = Column(Text)
    detailed_description = Column(Text, nullable=True)
    start_date = Column(Date)
    end_date = Column(Date)
    status_by_day = Column(JSON, default={})

    subsystem = relationship("Subsystem", back_populates="tasks")
    team = relationship("Team", back_populates="tasks")