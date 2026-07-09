from fastapi import FastAPI

from app.core.database import Base, engine
from app.models import User, Roadmap
from app.routers.auth import router as auth_router
from app.routers.roadmap import router as roadmap_router
from app.routers.profile import router as profile_router
from app.routers.workout_plan import router as workout_plan_router
from app.routers.workout_day import router as workout_day_router
from app.routers.exercise import router as exercise_router
from app.routers.workout_session import router as workout_session_router
from app.routers.exercise_log import router as exercise_log_router
from app.routers.set_log import router as set_log_router
from app.routers.workout_day_exercise import router as workout_day_exercise_router


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
app.include_router(workout_day_router)
app.include_router(workout_day_exercise_router)  
app.include_router(workout_session_router)
app.include_router(exercise_log_router)
app.include_router(set_log_router)

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