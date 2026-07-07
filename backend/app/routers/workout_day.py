from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.core.database import get_db

from app.models.user import User
from app.models.workout_plan import WorkoutPlan
from app.models.workout_day import WorkoutDay

from app.schemas.workout_day import (
    WorkoutDayCreate,
    WorkoutDayUpdate,
    WorkoutDayResponse,
)

router = APIRouter(
    prefix="/workout-days",
    tags=["Workout Days"],
)


# Create a workout day
@router.post("/", response_model=WorkoutDayResponse)
def create_workout_day(
    workout_day: WorkoutDayCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    workout_plan = (
        db.query(WorkoutPlan)
        .filter(
            WorkoutPlan.id == workout_day.workout_plan_id,
            WorkoutPlan.owner_id == current_user.id,
        )
        .first()
    )

    if not workout_plan:
        raise HTTPException(
            status_code=404,
            detail="Workout plan not found",
        )

    new_day = WorkoutDay(
        name=workout_day.name,
        day_of_week=workout_day.day_of_week,
        order=workout_day.order,
        workout_plan_id=workout_day.workout_plan_id,
    )

    db.add(new_day)
    db.commit()
    db.refresh(new_day)

    return new_day


# Get all workout days
@router.get("/", response_model=list[WorkoutDayResponse])
def get_workout_days(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return (
        db.query(WorkoutDay)
        .join(WorkoutPlan)
        .filter(WorkoutPlan.owner_id == current_user.id)
        .order_by(WorkoutDay.order)
        .all()
    )


# Get a single workout day
@router.get("/{day_id}", response_model=WorkoutDayResponse)
def get_workout_day(
    day_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    day = (
        db.query(WorkoutDay)
        .join(WorkoutPlan)
        .filter(
            WorkoutDay.id == day_id,
            WorkoutPlan.owner_id == current_user.id,
        )
        .first()
    )

    if not day:
        raise HTTPException(
            status_code=404,
            detail="Workout day not found",
        )

    return day


# Update a workout day
@router.put("/{day_id}", response_model=WorkoutDayResponse)
def update_workout_day(
    day_id: int,
    workout_day: WorkoutDayUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    day = (
        db.query(WorkoutDay)
        .join(WorkoutPlan)
        .filter(
            WorkoutDay.id == day_id,
            WorkoutPlan.owner_id == current_user.id,
        )
        .first()
    )

    if not day:
        raise HTTPException(
            status_code=404,
            detail="Workout day not found",
        )

    update_data = workout_day.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(day, key, value)

    db.commit()
    db.refresh(day)

    return day


# Delete a workout day
@router.delete("/{day_id}")
def delete_workout_day(
    day_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    day = (
        db.query(WorkoutDay)
        .join(WorkoutPlan)
        .filter(
            WorkoutDay.id == day_id,
            WorkoutPlan.owner_id == current_user.id,
        )
        .first()
    )

    if not day:
        raise HTTPException(
            status_code=404,
            detail="Workout day not found",
        )

    db.delete(day)
    db.commit()

    return {
        "message": "Workout day deleted successfully"
    }