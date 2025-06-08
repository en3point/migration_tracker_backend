from fastapi import APIRouter
from app.api.endpoints import tasks, task_buckets

router = APIRouter()
router.include_router(tasks.router, prefix="", tags=["Tasks"])
router.include_router(task_buckets.router, prefix="", tags=["Task Buckets"])
