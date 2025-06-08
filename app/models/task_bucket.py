from sqlalchemy import Column, Integer, String
from app.db.database import Base

class TaskBucket(Base):
    __tablename__ = "task_buckets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    order = Column(Integer, nullable=False)
