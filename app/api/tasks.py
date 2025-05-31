from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.models import Task, Team, Subsystem, ProjectPhase
from pydantic import BaseModel
from typing import List, Optional
from datetime import date

router = APIRouter()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ------------------ TASK SCHEMAS ------------------
class TaskBase(BaseModel):
    subsystem_id: int
    team_id: int
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

# ------------------ TASK ENDPOINTS ------------------
@router.post("/tasks/", response_model=TaskOut)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    db_task = Task(**task.dict())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

@router.get("/tasks/", response_model=List[TaskOut])
def read_tasks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(Task).offset(skip).limit(limit).all()

@router.get("/tasks/{task_id}", response_model=TaskOut)
def read_task(task_id: int, db: Session = Depends(get_db)):
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task

@router.put("/tasks/{task_id}", response_model=TaskOut)
def update_task(task_id: int, task: TaskUpdate, db: Session = Depends(get_db)):
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    for key, value in task.dict().items():
        setattr(db_task, key, value)
    db.commit()
    db.refresh(db_task)
    return db_task

@router.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(db_task)
    db.commit()
    return {"message": "Task deleted successfully"}

# ------------------ TEAM ENDPOINTS ------------------
@router.post("/teams/", response_model=TeamOut)
def create_team(team: TeamCreate, db: Session = Depends(get_db)):
    db_team = Team(**team.dict())
    db.add(db_team)
    db.commit()
    db.refresh(db_team)
    return db_team

@router.get("/teams/", response_model=List[TeamOut])
def read_teams(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(Team).offset(skip).limit(limit).all()

# ------------------ SUBSYSTEM ENDPOINTS ------------------
@router.post("/subsystems/", response_model=SubsystemOut)
def create_subsystem(subsystem: SubsystemCreate, db: Session = Depends(get_db)):
    db_subsystem = Subsystem(**subsystem.dict())
    db.add(db_subsystem)
    db.commit()
    db.refresh(db_subsystem)
    return db_subsystem

@router.get("/subsystems/", response_model=List[SubsystemOut])
def read_subsystems(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(Subsystem).offset(skip).limit(limit).all()

# ------------------ PROJECT PHASE ENDPOINTS ------------------
@router.post("/phases/", response_model=ProjectPhaseOut)
def create_project_phase(phase: ProjectPhaseCreate, db: Session = Depends(get_db)):
    db_phase = ProjectPhase(**phase.dict())
    db.add(db_phase)
    db.commit()
    db.refresh(db_phase)
    return db_phase

@router.get("/phases/", response_model=List[ProjectPhaseOut])
def read_project_phases(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(ProjectPhase).offset(skip).limit(limit).all()
