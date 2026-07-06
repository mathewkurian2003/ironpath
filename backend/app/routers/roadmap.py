from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.core.database import get_db
from app.models.user import User
from app.schemas.roadmap import RoadmapCreate, RoadmapResponse
from app.services.roadmap_service import create_roadmap

router = APIRouter(
    prefix="/roadmaps",
    tags=["Roadmaps"],
)


@router.post("/", response_model=RoadmapResponse)
def create_new_roadmap(
    roadmap: RoadmapCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_roadmap(
        db=db,
        roadmap=roadmap,
        current_user=current_user,
    )