# schemas.py
from pydantic import BaseModel
from typing import Optional, Dict
from datetime import date

class TeamBase(BaseModel):
    name: str
    email_to: Optional[str] = None
    email_cc: Optional[str] = None

class TeamCreate(TeamBase):
    pass

class TeamRead(TeamBase):
    id: int
    class Config:
        orm_mode = True

class SubsystemBase(BaseModel):
    name: str

class SubsystemCreate(SubsystemBase):
    pass

class SubsystemRead(SubsystemBase):
    id: int
    class Config:
        orm_mode = True

class ProjectPhaseBase(BaseModel):
    date: date
    label: str

class ProjectPhaseCreate(ProjectPhaseBase):
    pass

class ProjectPhaseRead(ProjectPhaseBase):
    id: int
    class Config:
        orm_mode = True

class TaskBase(BaseModel):
    subsystem_id: int
    team_id: Optional[int] = None
    vendor_system: Optional[str] = None
    subject: str
    description: str
    detailed_description: Optional[str] = None
    start_date: date
    end_date: date
    status_by_day: Optional[Dict[str, str]] = {}

class TaskCreate(TaskBase):
    pass

class TaskRead(TaskBase):
    id: int
    class Config:
        orm_mode = True
