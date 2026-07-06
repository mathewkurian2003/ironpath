from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.core.database import get_db
from app.models.user import User
from app.models.workout_plan import WorkoutPlan

from app.schemas.workout_plan import (
    WorkoutPlanCreate,
    WorkoutPlanUpdate,
    WorkoutPlanResponse,
)

router = APIRouter(
    prefix="/workout-plans",
    tags=["Workout Plans"],
)


# Create a workout plan
@router.post("/", response_model=WorkoutPlanResponse)
def create_workout_plan(
    workout_plan: WorkoutPlanCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    new_plan = WorkoutPlan(
        name=workout_plan.name,
        description=workout_plan.description,
        owner_id=current_user.id,
    )

    db.add(new_plan)
    db.commit()
    db.refresh(new_plan)

    return new_plan


# Get all workout plans for the current user
@router.get("/", response_model=list[WorkoutPlanResponse])
def get_workout_plans(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return (
        db.query(WorkoutPlan)
        .filter(WorkoutPlan.owner_id == current_user.id)
        .all()
    )


# Get a single workout plan
@router.get("/{plan_id}", response_model=WorkoutPlanResponse)
def get_workout_plan(
    plan_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    plan = (
        db.query(WorkoutPlan)
        .filter(
            WorkoutPlan.id == plan_id,
            WorkoutPlan.owner_id == current_user.id,
        )
        .first()
    )

    if not plan:
        raise HTTPException(
            status_code=404,
            detail="Workout plan not found",
        )

    return plan


# Update a workout plan
@router.put("/{plan_id}", response_model=WorkoutPlanResponse)
def update_workout_plan(
    plan_id: int,
    workout_plan: WorkoutPlanUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    plan = (
        db.query(WorkoutPlan)
        .filter(
            WorkoutPlan.id == plan_id,
            WorkoutPlan.owner_id == current_user.id,
        )
        .first()
    )

    if not plan:
        raise HTTPException(
            status_code=404,
            detail="Workout plan not found",
        )

    update_data = workout_plan.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(plan, key, value)

    db.commit()
    db.refresh(plan)

    return plan


# Delete a workout plan
@router.delete("/{plan_id}")
def delete_workout_plan(
    plan_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    plan = (
        db.query(WorkoutPlan)
        .filter(
            WorkoutPlan.id == plan_id,
            WorkoutPlan.owner_id == current_user.id,
        )
        .first()
    )

    if not plan:
        raise HTTPException(
            status_code=404,
            detail="Workout plan not found",
        )

    db.delete(plan)
    db.commit()

    return {
        "message": "Workout plan deleted successfully"
    }