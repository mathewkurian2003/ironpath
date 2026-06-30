from fastapi import FastAPI

from app.core.database import Base, engine
from app.models import User, Interview
from app.routers.auth import router as auth_router

# Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="IronPath API",
    description="AI-powered gym progression platform",
    version="1.0.0"
)

app.include_router(auth_router)


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