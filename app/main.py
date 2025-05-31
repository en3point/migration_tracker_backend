from fastapi import FastAPI
from app.api import tasks  # Import your task router

app = FastAPI()

# Register the router
app.include_router(tasks.router, prefix="", tags=["Tasks"])
