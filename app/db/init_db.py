
from app.db.database import engine
from app.models import *
from app.db.database import Base

def init_db():
    Base.metadata.create_all(bind=engine)
