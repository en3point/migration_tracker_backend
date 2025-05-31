from sqlalchemy import Column, Integer, String, Text, Date, ForeignKey
from sqlalchemy.dialects.sqlite import JSON
from app.db.database import Base

class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    subsystem_id = Column(Integer, ForeignKey("subsystems.id"))
    team_id = Column(Integer, ForeignKey("teams.id"))
    vendor_system = Column(String)
    subject = Column(String)
    description = Column(String)
    detailed_description = Column(Text)
    start_date = Column(Date)
    end_date = Column(Date)
    status_by_day = Column(JSON, default={})