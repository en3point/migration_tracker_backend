# api/endpoints.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import models, schemas
from app.db.database import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Teams
@router.post("/teams/", response_model=schemas.TeamRead)
def create_team(team: schemas.TeamCreate, db: Session = Depends(get_db)):
    db_team = models.Team(**team.dict())
    db.add(db_team)
    db.commit()
    db.refresh(db_team)
    return db_team

@router.get("/teams/", response_model=list[schemas.TeamRead])
def read_teams(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.Team).offset(skip).limit(limit).all()

@router.put("/teams/{team_id}", response_model=schemas.TeamRead)
def update_team(team_id: int, update: schemas.TeamUpdate, db: Session = Depends(get_db)):
    db_team = db.query(models.Team).get(team_id)
    if not db_team:
        raise HTTPException(status_code=404, detail="Team not found")
    for field, value in update.dict().items():
        setattr(db_team, field, value)
    db.commit()
    db.refresh(db_team)
    return db_team

@router.delete("/teams/{team_id}")
def delete_team(team_id: int, db: Session = Depends(get_db)):
    db_team = db.query(models.Team).get(team_id)
    if not db_team:
        raise HTTPException(status_code=404, detail="Team not found")
    db.delete(db_team)
    db.commit()
    return {"ok": True}

# Subsystems
@router.post("/subsystems/", response_model=schemas.SubsystemRead)
def create_subsystem(subsystem: schemas.SubsystemCreate, db: Session = Depends(get_db)):
    db_subsystem = models.Subsystem(**subsystem.dict())
    db.add(db_subsystem)
    db.commit()
    db.refresh(db_subsystem)
    return db_subsystem

@router.get("/subsystems/", response_model=list[schemas.SubsystemRead])
def read_subsystems(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.Subsystem).offset(skip).limit(limit).all()

@router.put("/subsystems/{subsystem_id}", response_model=schemas.SubsystemRead)
def update_subsystem(subsystem_id: int, update: schemas.SubsystemUpdate, db: Session = Depends(get_db)):
    db_subsystem = db.query(models.Subsystem).get(subsystem_id)
    if not db_subsystem:
        raise HTTPException(status_code=404, detail="Subsystem not found")
    for field, value in update.dict().items():
        setattr(db_subsystem, field, value)
    db.commit()
    db.refresh(db_subsystem)
    return db_subsystem

@router.delete("/subsystems/{subsystem_id}")
def delete_subsystem(subsystem_id: int, db: Session = Depends(get_db)):
    db_subsystem = db.query(models.Subsystem).get(subsystem_id)
    if not db_subsystem:
        raise HTTPException(status_code=404, detail="Subsystem not found")
    db.delete(db_subsystem)
    db.commit()
    return {"ok": True}

# Project Phases
@router.post("/phases/", response_model=schemas.ProjectPhaseRead)
def create_phase(phase: schemas.ProjectPhaseCreate, db: Session = Depends(get_db)):
    db_phase = models.ProjectPhase(**phase.dict())
    db.add(db_phase)
    db.commit()
    db.refresh(db_phase)
    return db_phase

@router.get("/phases/", response_model=list[schemas.ProjectPhaseRead])
def read_phases(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.ProjectPhase).offset(skip).limit(limit).all()

@router.put("/phases/{phase_id}", response_model=schemas.ProjectPhaseRead)
def update_phase(phase_id: int, update: schemas.ProjectPhaseUpdate, db: Session = Depends(get_db)):
    db_phase = db.query(models.ProjectPhase).get(phase_id)
    if not db_phase:
        raise HTTPException(status_code=404, detail="Phase not found")
    for field, value in update.dict().items():
        setattr(db_phase, field, value)
    db.commit()
    db.refresh(db_phase)
    return db_phase

@router.delete("/phases/{phase_id}")
def delete_phase(phase_id: int, db: Session = Depends(get_db)):
    db_phase = db.query(models.ProjectPhase).get(phase_id)
    if not db_phase:
        raise HTTPException(status_code=404, detail="Phase not found")
    db.delete(db_phase)
    db.commit()
    return {"ok": True}
