# app/api/endpoints/tasks.py
from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.models import Task, TaskBucket, Subsystem
from app.db import schemas
from io import BytesIO
import pandas as pd
from typing import List, Optional
from datetime import date

router = APIRouter()

# ------------------ DB DEPENDENCY ------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ------------------ TASK ENDPOINTS ------------------
@router.post("/tasks/", response_model=schemas.TaskOut)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    task_bucket = db.query(TaskBucket).filter(TaskBucket.id == task.task_bucket_id).first()
    if not task_bucket:
        raise HTTPException(status_code=400, detail="TaskBucket does not exist")

    db_task = Task(**task.dict())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

@router.get("/tasks/", response_model=List[schemas.TaskOut])
def read_tasks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(Task).offset(skip).limit(limit).all()

@router.get("/tasks/{task_id}", response_model=schemas.TaskOut)
def read_task(task_id: int, db: Session = Depends(get_db)):
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task

@router.put("/tasks/{task_id}", response_model=schemas.TaskOut)
def update_task(task_id: int, task: schemas.TaskUpdate, db: Session = Depends(get_db)):
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

# ------------------ DAILY SUMMARY ENDPOINT ------------------
@router.get("/daily-summary/", response_model=schemas.DailySummary)
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
        serialized = schemas.TaskOut.from_orm(task)
        if status.lower() == "done":
            completed.append(serialized)
        else:
            pending.append(serialized)

    return schemas.DailySummary(
        date=date_query,
        subsystem_id=subsystem_id,
        team_id=team_id,
        completed_tasks=completed,
        pending_tasks=pending
    )
