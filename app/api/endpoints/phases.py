# app/api/endpoints/phases.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.models import ProjectPhase, Project
from app.db import schemas
from typing import List

router = APIRouter(tags=["Phases"])

# ------------------ DB DEPENDENCY ------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ------------------ PROJECT PHASE ENDPOINTS ------------------
@router.post("/phases/", response_model=schemas.ProjectPhaseOut)
def create_phase(phase: schemas.ProjectPhaseCreate, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == phase.project_id).first()
    if not project:
        raise HTTPException(status_code=400, detail="Project does not exist")

    max_order = db.query(ProjectPhase).filter(ProjectPhase.project_id == phase.project_id).count()
    db_phase = ProjectPhase(**phase.dict(), order=max_order + 1)
    db.add(db_phase)
    db.commit()
    db.refresh(db_phase)
    return db_phase

@router.get("/phases/", response_model=List[schemas.ProjectPhaseOut])
def read_phases(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(ProjectPhase).order_by(ProjectPhase.order).offset(skip).limit(limit).all()

@router.get("/phases/by-project/{project_id}", response_model=List[schemas.ProjectPhaseOut])
def read_phases_by_project(project_id: int, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    return db.query(ProjectPhase).filter(ProjectPhase.project_id == project_id).order_by(ProjectPhase.order).all()

@router.get("/phases/{phase_id}", response_model=schemas.ProjectPhaseOut)
def read_phase(phase_id: int, db: Session = Depends(get_db)):
    db_phase = db.query(ProjectPhase).filter(ProjectPhase.id == phase_id).first()
    if not db_phase:
        raise HTTPException(status_code=404, detail="Phase not found")
    return db_phase

@router.put("/phases/{phase_id}", response_model=schemas.ProjectPhaseOut)
def update_phase(phase_id: int, phase: schemas.ProjectPhaseUpdate, db: Session = Depends(get_db)):
    db_phase = db.query(ProjectPhase).filter(ProjectPhase.id == phase_id).first()
    if not db_phase:
        raise HTTPException(status_code=404, detail="Phase not found")
    for key, value in phase.dict().items():
        setattr(db_phase, key, value)
    db.commit()
    db.refresh(db_phase)
    return db_phase

@router.delete("/phases/{phase_id}")
def delete_phase(phase_id: int, db: Session = Depends(get_db)):
    db_phase = db.query(ProjectPhase).filter(ProjectPhase.id == phase_id).first()
    if not db_phase:
        raise HTTPException(status_code=404, detail="Phase not found")
    db.delete(db_phase)
    db.commit()
    return {"message": "Phase deleted successfully"}
