from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.models import Subsystem
from app.db import schemas
from typing import List

router = APIRouter(tags=["SubSystems"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/subsystems/", response_model=schemas.SubsystemOut)
def create_subsystem(subsystem: schemas.SubsystemCreate, db: Session = Depends(get_db)):
    db_subsystem = Subsystem(**subsystem.dict())
    db.add(db_subsystem)
    db.commit()
    db.refresh(db_subsystem)
    return db_subsystem

@router.get("/subsystems/", response_model=List[schemas.SubsystemOut])
def read_subsystems(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(Subsystem).offset(skip).limit(limit).all()

@router.put("/subsystems/{subsystem_id}", response_model=schemas.SubsystemOut)
def update_subsystem(subsystem_id: int, subsystem: schemas.SubsystemCreate, db: Session = Depends(get_db)):
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
