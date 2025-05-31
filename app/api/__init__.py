from fastapi import APIRouter
from . import tasks

router = APIRouter()
router.include_router(tasks.router, prefix="", tags=["Tasks"])
