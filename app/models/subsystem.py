from sqlalchemy import Column, Integer, String
from app.db.database import Base

class Subsystem(Base):
    __tablename__ = "subsystems"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)