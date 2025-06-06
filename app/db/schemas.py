# app/db/schemas.py
from pydantic import BaseModel
from typing import Optional, List
from datetime import date

# ------------------ TASK SCHEMAS ------------------
class TaskBase(BaseModel):
    subsystem_id: int
    team_id: Optional[int] = None
    vendor_system: Optional[str] = None
    subject: str
    description: str
    detailed_description: Optional[str] = None
    start_date: date
    end_date: date
    status_by_day: Optional[dict] = {}

class TaskCreate(TaskBase):
    pass

class TaskUpdate(TaskBase):
    pass

class TaskOut(TaskBase):
    id: int

    class Config:
        orm_mode = True

# ------------------ TEAM SCHEMAS ------------------
class TeamBase(BaseModel):
    name: str
    email_to: Optional[str] = None
    email_cc: Optional[str] = None

class TeamCreate(TeamBase):
    pass

class TeamOut(TeamBase):
    id: int

    class Config:
        orm_mode = True

# ------------------ SUBSYSTEM SCHEMAS ------------------
class SubsystemBase(BaseModel):
    name: str

class SubsystemCreate(SubsystemBase):
    pass

class SubsystemOut(SubsystemBase):
    id: int

    class Config:
        orm_mode = True

# ------------------ PROJECT PHASE SCHEMAS ------------------
class ProjectPhaseBase(BaseModel):
    date: date
    label: str

class ProjectPhaseCreate(ProjectPhaseBase):
    pass

class ProjectPhaseOut(ProjectPhaseBase):
    id: int

    class Config:
        orm_mode = True

# ------------------ DAILY SUMMARY SCHEMA ------------------
class DailySummary(BaseModel):
    date: date
    subsystem_id: Optional[int] = None
    team_id: Optional[int] = None
    completed_tasks: List[TaskOut]
    pending_tasks: List[TaskOut]
