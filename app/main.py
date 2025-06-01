from fastapi import FastAPI
from app.api import router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()  # ✅ must come first

# ✅ then apply CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to frontend domain if needed later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ then include your API router
app.include_router(router)
