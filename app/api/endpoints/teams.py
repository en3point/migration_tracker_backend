from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.models import Team
from app.db import schemas
from typing import List

router = APIRouter(tags=["Teams"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/teams/", response_model=schemas.TeamOut)
def create_team(team: schemas.TeamCreate, db: Session = Depends(get_db)):
    db_team = Team(**team.dict())
    db.add(db_team)
    db.commit()
    db.refresh(db_team)
    return db_team

@router.get("/teams/", response_model=List[schemas.TeamOut])
def read_teams(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(Team).offset(skip).limit(limit).all()

@router.put("/teams/{team_id}", response_model=schemas.TeamOut)
def update_team(team_id: int, team: schemas.TeamCreate, db: Session = Depends(get_db)):
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
