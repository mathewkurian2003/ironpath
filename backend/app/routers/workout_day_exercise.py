from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models import WorkoutDay, WorkoutDayExercise
from app.schemas import (
    WorkoutDayExerciseCreate,
    WorkoutDayExerciseUpdate,
    WorkoutDayExerciseResponse,
)

router = APIRouter(
    prefix="/workout-days/{workout_day_id}/exercises",
    tags=["Workout Day Exercises"],
)


@router.post(
    "/",
    response_model=WorkoutDayExerciseResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_workout_day_exercise(
    workout_day_id: int,
    exercise: WorkoutDayExerciseCreate,
    db: Session = Depends(get_db),
):
    workout_day = (
        db.query(WorkoutDay)
        .filter(WorkoutDay.id == workout_day_id)
        .first()
    )

    if not workout_day:
        raise HTTPException(
            status_code=404,
            detail="Workout day not found",
        )

    db_exercise = WorkoutDayExercise(
        workout_day_id=workout_day_id,
        **exercise.model_dump(),
    )

    db.add(db_exercise)
    db.commit()
    db.refresh(db_exercise)

    return db_exercise


@router.get(
    "/",
    response_model=list[WorkoutDayExerciseResponse],
)
def get_workout_day_exercises(
    workout_day_id: int,
    db: Session = Depends(get_db),
):
    return (
        db.query(WorkoutDayExercise)
        .filter(
            WorkoutDayExercise.workout_day_id == workout_day_id
        )
        .order_by(WorkoutDayExercise.order)
        .all()
    )


@router.get(
    "/{exercise_id}",
    response_model=WorkoutDayExerciseResponse,
)
def get_workout_day_exercise(
    workout_day_id: int,
    exercise_id: int,
    db: Session = Depends(get_db),
):
    exercise = (
        db.query(WorkoutDayExercise)
        .filter(
            WorkoutDayExercise.id == exercise_id,
            WorkoutDayExercise.workout_day_id == workout_day_id,
        )
        .first()
    )

    if not exercise:
        raise HTTPException(
            status_code=404,
            detail="Workout day exercise not found",
        )

    return exercise


@router.put(
    "/{exercise_id}",
    response_model=WorkoutDayExerciseResponse,
)
def update_workout_day_exercise(
    workout_day_id: int,
    exercise_id: int,
    exercise_update: WorkoutDayExerciseUpdate,
    db: Session = Depends(get_db),
):
    exercise = (
        db.query(WorkoutDayExercise)
        .filter(
            WorkoutDayExercise.id == exercise_id,
            WorkoutDayExercise.workout_day_id == workout_day_id,
        )
        .first()
    )

    if not exercise:
        raise HTTPException(
            status_code=404,
            detail="Workout day exercise not found",
        )

    update_data = exercise_update.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(exercise, key, value)

    db.commit()
    db.refresh(exercise)

    return exercise


@router.delete(
    "/{exercise_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_workout_day_exercise(
    workout_day_id: int,
    exercise_id: int,
    db: Session = Depends(get_db),
):
    exercise = (
        db.query(WorkoutDayExercise)
        .filter(
            WorkoutDayExercise.id == exercise_id,
            WorkoutDayExercise.workout_day_id == workout_day_id,
        )
        .first()
    )

    if not exercise:
        raise HTTPException(
            status_code=404,
            detail="Workout day exercise not found",
        )

    db.delete(exercise)
    db.commit()