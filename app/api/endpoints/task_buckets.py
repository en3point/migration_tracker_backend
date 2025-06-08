from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.models import TaskBucket, Task
from app.db import schemas
from typing import List

router = APIRouter()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ------------------ TaskBucket CRUD ------------------
@router.post("/task-buckets/", response_model=schemas.TaskBucketOut)
def create_task_bucket(bucket: schemas.TaskBucketCreate, db: Session = Depends(get_db)):
    db_bucket = TaskBucket(**bucket.dict())
    db.add(db_bucket)
    db.commit()
    db.refresh(db_bucket)
    return db_bucket

@router.get("/task-buckets/", response_model=List[schemas.TaskBucketOut])
def read_task_buckets(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(TaskBucket).offset(skip).limit(limit).all()

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
    db_bucket = db.query(TaskBucket).filter(TaskBucket.id == bucket_id).first()
    if not db_bucket:
        raise HTTPException(status_code=404, detail="TaskBucket not found")
    
    if db.query(Task).filter(Task.task_bucket_id == bucket_id).first():
        raise HTTPException(status_code=400, detail="Cannot delete TaskBucket with existing tasks.")
    
    db.delete(db_bucket)
    db.commit()
    return {"message": "TaskBucket deleted successfully"}
