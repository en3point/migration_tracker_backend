// app/api/endpoints/tasks.py (routes only)
from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.db.models import Task, Team, Subsystem, ProjectPhase
from app.db.schemas import TaskCreate, TaskUpdate, TaskOut, TeamCreate, TeamOut, SubsystemCreate, SubsystemOut, ProjectPhaseCreate, ProjectPhaseOut, DailySummary
from datetime import date
from typing import List, Optional
import pandas as pd
from io import BytesIO

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

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

@router.put("/teams/{team_id}", response_model=TeamOut)
def update_team(team_id: int, team: TeamCreate, db: Session = Depends(get_db)):
    db_team = db.query(Team).filter(Team.id == team_id).first()
    if not db_team:
        raise HTTPException(status_code=404, detail="Team not found")
    for key, value in team.dict().items():
        setattr(db_team, key, value)
    db.commit()
    db.refresh(db_team)
    return db_team

@router.delete("/teams/{team_id}")
def delete_team(team_id: int, db: Session = Depends(get_db)):
    db_team = db.query(Team).filter(Team.id == team_id).first()
    if not db_team:
        raise HTTPException(status_code=404, detail="Team not found")
    db.delete(db_team)
    db.commit()
    return {"message": "Team deleted successfully"}

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

@router.put("/subsystems/{subsystem_id}", response_model=SubsystemOut)
def update_subsystem(subsystem_id: int, subsystem: SubsystemCreate, db: Session = Depends(get_db)):
    db_subsystem = db.query(Subsystem).filter(Subsystem.id == subsystem_id).first()
    if not db_subsystem:
        raise HTTPException(status_code=404, detail="Subsystem not found")
    for key, value in subsystem.dict().items():
        setattr(db_subsystem, key, value)
    db.commit()
    db.refresh(db_subsystem)
    return db_subsystem

@router.delete("/subsystems/{subsystem_id}")
def delete_subsystem(subsystem_id: int, db: Session = Depends(get_db)):
    db_subsystem = db.query(Subsystem).filter(Subsystem.id == subsystem_id).first()
    if not db_subsystem:
        raise HTTPException(status_code=404, detail="Subsystem not found")
    db.delete(db_subsystem)
    db.commit()
    return {"message": "Subsystem deleted successfully"}

# ------------------ PHASE ENDPOINTS ------------------
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

@router.put("/phases/{phase_id}", response_model=ProjectPhaseOut)
def update_project_phase(phase_id: int, phase: ProjectPhaseCreate, db: Session = Depends(get_db)):
    db_phase = db.query(ProjectPhase).filter(ProjectPhase.id == phase_id).first()
    if not db_phase:
        raise HTTPException(status_code=404, detail="Project phase not found")
    for key, value in phase.dict().items():
        setattr(db_phase, key, value)
    db.commit()
    db.refresh(db_phase)
    return db_phase

@router.delete("/phases/{phase_id}")
def delete_project_phase(phase_id: int, db: Session = Depends(get_db)):
    db_phase = db.query(ProjectPhase).filter(ProjectPhase.id == phase_id).first()
    if not db_phase:
        raise HTTPException(status_code=404, detail="Project phase not found")
    db.delete(db_phase)
    db.commit()
    return {"message": "Project phase deleted successfully"}

# ------------------ DAILY SUMMARY ------------------
@router.get("/daily-summary/", response_model=DailySummary)
def get_daily_summary(
    date_query: date,
    subsystem_id: Optional[int] = None,
    team_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Task).filter(
        Task.start_date <= date_query,
        Task.end_date >= date_query
    )
    if subsystem_id:
        query = query.filter(Task.subsystem_id == subsystem_id)
    if team_id:
        query = query.filter(Task.team_id == team_id)

    tasks = query.all()
    completed = []
    pending = []

    for task in tasks:
        status = task.status_by_day.get(str(date_query), "Pending")
        serialized = TaskOut.from_orm(task)
        if status.lower() == "done":
            completed.append(serialized)
        else:
            pending.append(serialized)

    return DailySummary(
        date=date_query,
        subsystem_id=subsystem_id,
        team_id=team_id,
        completed_tasks=completed,
        pending_tasks=pending
    )

# ------------------ EXCEL IMPORT ------------------
@router.post("/import-excel/")
def import_excel(file: UploadFile = File(...), db: Session = Depends(get_db)):
    content = file.file.read()
    excel_data = pd.read_excel(BytesIO(content), sheet_name=None)

    master_df = excel_data.get("MasterData")
    overview_df = excel_data.get("Overview")

    if master_df is not None:
        for _, row in master_df.iterrows():
            team_name = row.get("Unnamed: 1")
            email_to = row.get("Unnamed: 2")
            email_cc = row.get("Unnamed: 3")
            if pd.notna(team_name) and team_name != "Team":
                if not db.query(Team).filter_by(name=team_name).first():
                    db_team = Team(name=team_name, email_to=email_to, email_cc=email_cc)
                    db.add(db_team)

            date_val = row.get("Unnamed: 8")
            label_val = row.get("Unnamed: 9")
            if pd.notna(date_val) and pd.notna(label_val):
                if not db.query(ProjectPhase).filter_by(date=date_val).first():
                    db_phase = ProjectPhase(date=date_val, label=label_val)
                    db.add(db_phase)

    if overview_df is not None:
        for _, row in overview_df.iterrows():
            subsystem_name = row.get("Unnamed: 2")
            vendor_system = row.get("Unnamed: 3")
            subject = row.get("Unnamed: 4")
            description = row.get("Unnamed: 4")
            detailed_description = row.get("Unnamed: 50")
            if pd.notna(subsystem_name) and subsystem_name != "Subsystem":
                subsystem = db.query(Subsystem).filter_by(name=subsystem_name).first()
                if not subsystem:
                    subsystem = Subsystem(name=subsystem_name)
                    db.add(subsystem)
                    db.commit()
                    db.refresh(subsystem)

                task = Task(
                    subsystem_id=subsystem.id,
                    team_id=None,
                    vendor_system=vendor_system,
                    subject=subject,
                    description=description,
                    detailed_description=detailed_description,
                    start_date=pd.to_datetime("2025-03-01"),
                    end_date=pd.to_datetime("2025-04-01"),
                    status_by_day={}
                )
                db.add(task)

    db.commit()
    return {"message": "Excel data imported successfully"}
