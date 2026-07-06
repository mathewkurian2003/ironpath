from fastapi import FastAPI

from app.core.database import Base, engine
from app.models import User, Roadmap
from app.routers.auth import router as auth_router
from app.routers.roadmap import router as roadmap_router
from app.routers.profile import router as profile_router
from app.routers.workout_plan import router as workout_plan_router
# Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="IronPath API",
    description="AI-powered gym progression platform",
    version="1.0.0"
)

app.include_router(auth_router)
app.include_router(roadmap_router)
app.include_router(profile_router)
app.include_router(workout_plan_router)


@app.get("/")
def root():
    return {
        "message": "Welcome to IronPath 🚀"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }