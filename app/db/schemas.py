# app/db/schemas.py
from pydantic import BaseModel
from typing import Optional, List, Dict
from datetime import date

# ------------------ TASK BUCKET ------------------
class TaskBucketBase(BaseModel):
    name: str
    order: int
    phase_id: int  # ✅ This is required for linking

class TaskBucketCreate(TaskBucketBase):
    pass

class TaskBucketUpdate(BaseModel):
    name: Optional[str] = None
    order: Optional[int] = None
    phase_id: Optional[int] = None  # ✅ Also allow updating phase

class TaskBucketOut(TaskBucketBase):
    id: int

    class Config:
        from_attributes = True

# ------------------ TASK ------------------
class TaskBase(BaseModel):
    task_bucket_id: int
    subsystem_id: int
    team_id: int
    vendor_system: Optional[str] = None
    subject: str
    description: str
    detailed_description: Optional[str] = None
    start_date: date
    end_date: date
    status_by_day: Optional[Dict[str, str]] = {}
    order: int

class TaskCreate(TaskBase):
    pass

class TaskUpdate(TaskBase):
    pass

class TaskOut(TaskBase):
    id: int

    class Config:
        from_attributes = True

# ------------------ TEAM ------------------
class TeamBase(BaseModel):
    name: str
    email_to: Optional[str] = None
    email_cc: Optional[str] = None

class TeamCreate(TeamBase):
    pass

class TeamOut(TeamBase):
    id: int

    class Config:
        from_attributes = True

# ------------------ SUBSYSTEM ------------------
class SubsystemBase(BaseModel):
    name: str

class SubsystemCreate(SubsystemBase):
    pass

class SubsystemOut(SubsystemBase):
    id: int

    class Config:
        from_attributes = True

# ------------------ PROJECT PHASE ------------------
class ProjectPhaseBase(BaseModel):
    date: date
    label: str

class ProjectPhaseCreate(ProjectPhaseBase):
    pass

class ProjectPhaseOut(ProjectPhaseBase):
    id: int

class ProjectPhaseUpdate(BaseModel):
    name: Optional[str] = None
    order: Optional[int] = None

    class Config:
        from_attributes = True

# ------------------ DAILY SUMMARY ------------------
class DailySummary(BaseModel):
    date: date
    subsystem_id: Optional[int] = None
    team_id: Optional[int] = None
    completed_tasks: List[TaskOut]
    pending_tasks: List[TaskOut]
