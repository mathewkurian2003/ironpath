from sqlalchemy.orm import Session

from app.models.roadmap import Roadmap
from app.models.user import User
from app.schemas.roadmap import RoadmapCreate


def create_roadmap(
    db: Session,
    roadmap: RoadmapCreate,
    current_user: User,
):
    new_roadmap = Roadmap(
        title=roadmap.title,
        description=roadmap.description,
        target_date=roadmap.target_date,
        owner_id=current_user.id,
    )

    db.add(new_roadmap)
    db.commit()
    db.refresh(new_roadmap)

    return new_roadmap