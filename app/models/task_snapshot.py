from sqlalchemy import Column, Integer, String, Date, ForeignKey
from app.db.database import Base

class TaskStatusSnapshot(Base):
    __tablename__ = "task_snapshots"
    id = Column(Integer, primary_key=True)
    task_id = Column(Integer, ForeignKey("tasks.id"))
    date = Column(Date)
    status = Column(String)