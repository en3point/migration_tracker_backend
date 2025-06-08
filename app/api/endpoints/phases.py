from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.models import ProjectPhase
from app.db import schemas
from typing import List

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/phases/", response_model=schemas.ProjectPhaseOut)
def create_project_phase(phase: schemas.ProjectPhaseCreate, db: Session = Depends(get_db)):
    db_phase = ProjectPhase(**phase.dict())
    db.add(db_phase)
    db.commit()
    db.refresh(db_phase)
    return db_phase

@router.get("/phases/", response_model=List[schemas.ProjectPhaseOut])
def read_project_phases(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(ProjectPhase).offset(skip).limit(limit).all()

@router.put("/phases/{phase_id}", response_model=schemas.ProjectPhaseOut)
def update_project_phase(phase_id: int, phase: schemas.ProjectPhaseCreate, db: Session = Depends(get_db)):
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
