from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.core.database import get_db
from app.models.user import User
from app.models.profile import Profile
from app.schemas.profile import ProfileCreate, ProfileResponse

router = APIRouter(
    prefix="/profiles",
    tags=["Profiles"]
)


@router.post("/", response_model=ProfileResponse)
def create_or_update_profile(
    profile: ProfileCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    existing_profile = (
        db.query(Profile)
        .filter(Profile.user_id == current_user.id)
        .first()
    )

    if existing_profile:
        existing_profile.age = profile.age
        existing_profile.height = profile.height
        existing_profile.weight = profile.weight
        existing_profile.gender = profile.gender
        existing_profile.fitness_goal = profile.fitness_goal
        existing_profile.experience_level = profile.experience_level
        existing_profile.activity_level = profile.activity_level

        db.commit()
        db.refresh(existing_profile)

        return existing_profile

    new_profile = Profile(
        **profile.model_dump(),
        user_id=current_user.id
    )

    db.add(new_profile)
    db.commit()
    db.refresh(new_profile)

    return new_profile


@router.get("/me", response_model=ProfileResponse)
def get_my_profile(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    profile = (
        db.query(Profile)
        .filter(Profile.user_id == current_user.id)
        .first()
    )

    if not profile:
        raise HTTPException(
            status_code=404,
            detail="Profile not found"
        )

    return profile