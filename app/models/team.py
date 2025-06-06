from sqlalchemy import Column, Integer, String, Text
from app.db.database import Base

class Team(Base):
    __tablename__ = "teams"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    email_to = Column(Text)
    email_cc = Column(Text)