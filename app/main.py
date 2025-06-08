from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints.tasks import router as tasks_router
from app.api.endpoints.task_buckets import router as task_buckets_router
from app.api.endpoints.teams import router as teams_router
from app.api.endpoints.subsystems import router as subsystems_router
from app.api.endpoints.phases import router as phases_router
from app.db.database import Base, engine

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create DB tables
Base.metadata.create_all(bind=engine)

# Global error handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal Server Error"},
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Credentials": "true",
            "Access-Control-Allow-Methods": "*",
            "Access-Control-Allow-Headers": "*",
        },
    )

# Include routers
app.include_router(tasks_router)
app.include_router(task_buckets_router)
app.include_router(teams_router)
app.include_router(subsystems_router)
app.include_router(phases_router)
