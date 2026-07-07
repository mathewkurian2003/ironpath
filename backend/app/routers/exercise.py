from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.core.database import get_db

from app.models.user import User
from app.models.workout_plan import WorkoutPlan
from app.models.workout_day import WorkoutDay
from app.models.exercise import Exercise

from app.schemas.exercise import (
    ExerciseCreate,
    ExerciseUpdate,
    ExerciseResponse,
)

router = APIRouter(
    prefix="/exercises",
    tags=["Exercises"],
)


# Create an exercise
@router.post("/", response_model=ExerciseResponse)
def create_exercise(
    exercise: ExerciseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    workout_day = (
        db.query(WorkoutDay)
        .join(WorkoutPlan)
        .filter(
            WorkoutDay.id == exercise.workout_day_id,
            WorkoutPlan.owner_id == current_user.id,
        )
        .first()
    )

    if not workout_day:
        raise HTTPException(
            status_code=404,
            detail="Workout day not found",
        )

    new_exercise = Exercise(
        name=exercise.name,
        target_sets=exercise.target_sets,
        target_reps=exercise.target_reps,
        rest_time_seconds=exercise.rest_time_seconds,
        notes=exercise.notes,
        order=exercise.order,
        workout_day_id=exercise.workout_day_id,
    )

    db.add(new_exercise)
    db.commit()
    db.refresh(new_exercise)

    return new_exercise


# Get all exercises
@router.get("/", response_model=list[ExerciseResponse])
def get_exercises(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return (
        db.query(Exercise)
        .join(WorkoutDay)
        .join(WorkoutPlan)
        .filter(WorkoutPlan.owner_id == current_user.id)
        .order_by(Exercise.order)
        .all()
    )


# Get a single exercise
@router.get("/{exercise_id}", response_model=ExerciseResponse)
def get_exercise(
    exercise_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    exercise = (
        db.query(Exercise)
        .join(WorkoutDay)
        .join(WorkoutPlan)
        .filter(
            Exercise.id == exercise_id,
            WorkoutPlan.owner_id == current_user.id,
        )
        .first()
    )

    if not exercise:
        raise HTTPException(
            status_code=404,
            detail="Exercise not found",
        )

    return exercise


# Update an exercise
@router.put("/{exercise_id}", response_model=ExerciseResponse)
def update_exercise(
    exercise_id: int,
    exercise_update: ExerciseUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    exercise = (
        db.query(Exercise)
        .join(WorkoutDay)
        .join(WorkoutPlan)
        .filter(
            Exercise.id == exercise_id,
            WorkoutPlan.owner_id == current_user.id,
        )
        .first()
    )

    if not exercise:
        raise HTTPException(
            status_code=404,
            detail="Exercise not found",
        )

    update_data = exercise_update.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(exercise, key, value)

    db.commit()
    db.refresh(exercise)

    return exercise


# Delete an exercise
@router.delete("/{exercise_id}")
def delete_exercise(
    exercise_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    exercise = (
        db.query(Exercise)
        .join(WorkoutDay)
        .join(WorkoutPlan)
        .filter(
            Exercise.id == exercise_id,
            WorkoutPlan.owner_id == current_user.id,
        )
        .first()
    )

    if not exercise:
        raise HTTPException(
            status_code=404,
            detail="Exercise not found",
        )

    db.delete(exercise)
    db.commit()

    return {
        "message": "Exercise deleted successfully"
    }