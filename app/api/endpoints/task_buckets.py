# app/api/endpoints/task_buckets.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.models import TaskBucket, Task, ProjectPhase
from app.db import schemas
from typing import List

router = APIRouter(tags=["TaskBuckets"])

# ------------------ DB DEPENDENCY ------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ------------------ TASK BUCKET ENDPOINTS ------------------
@router.post("/task-buckets/", response_model=schemas.TaskBucketOut)
def create_task_bucket(bucket: schemas.TaskBucketCreate, db: Session = Depends(get_db)):
    phase = db.query(ProjectPhase).filter(ProjectPhase.id == bucket.phase_id).first()
    if not phase:
        raise HTTPException(status_code=400, detail="ProjectPhase does not exist")

    db_bucket = TaskBucket(**bucket.dict())
    db.add(db_bucket)
    db.commit()
    db.refresh(db_bucket)
    return db_bucket

@router.get("/task-buckets/", response_model=List[schemas.TaskBucketOut])
def read_task_buckets(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(TaskBucket).offset(skip).limit(limit).all()

@router.get("/task-buckets/{bucket_id}", response_model=schemas.TaskBucketOut)
def read_task_bucket(bucket_id: int, db: Session = Depends(get_db)):
    db_bucket = db.query(TaskBucket).filter(TaskBucket.id == bucket_id).first()
    if not db_bucket:
        raise HTTPException(status_code=404, detail="TaskBucket not found")
    return db_bucket

@router.put("/task-buckets/{bucket_id}", response_model=schemas.TaskBucketOut)
def update_task_bucket(bucket_id: int, bucket: schemas.TaskBucketUpdate, db: Session = Depends(get_db)):
    db_bucket = db.query(TaskBucket).filter(TaskBucket.id == bucket_id).first()
    if not db_bucket:
        raise HTTPException(status_code=404, detail="TaskBucket not found")
    for key, value in bucket.dict().items():
        setattr(db_bucket, key, value)
    db.commit()
    db.refresh(db_bucket)
    return db_bucket

@router.delete("/task-buckets/{bucket_id}")
def delete_task_bucket(bucket_id: int, db: Session = Depends(get_db)):
    if db.query(Task).filter(Task.task_bucket_id == bucket_id).count() > 0:
        raise HTTPException(status_code=400, detail="Cannot delete TaskBucket with associated Tasks")

    db_bucket = db.query(TaskBucket).filter(TaskBucket.id == bucket_id).first()
    if not db_bucket:
        raise HTTPException(status_code=404, detail="TaskBucket not found")
    db.delete(db_bucket)
    db.commit()
    return {"message": "TaskBucket deleted successfully"}
