from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.core.database import get_db

from app.models.user import User
from app.models.exercise import Exercise
from app.models.exercise_log import ExerciseLog
from app.models.workout_session import WorkoutSession

from app.schemas.exercise_log import (
    ExerciseLogCreate,
    ExerciseLogUpdate,
    ExerciseLogResponse,
)

router = APIRouter(
    prefix="/exercise-logs",
    tags=["Exercise Logs"],
)


# Create exercise log
@router.post("/", response_model=ExerciseLogResponse)
def create_exercise_log(
    exercise_log: ExerciseLogCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    workout_session = (
        db.query(WorkoutSession)
        .filter(
            WorkoutSession.id == exercise_log.workout_session_id,
            WorkoutSession.user_id == current_user.id,
        )
        .first()
    )

    if not workout_session:
        raise HTTPException(
            status_code=404,
            detail="Workout session not found",
        )

    exercise = (
        db.query(Exercise)
        .filter(Exercise.id == exercise_log.exercise_id)
        .first()
    )

    if not exercise:
        raise HTTPException(
            status_code=404,
            detail="Exercise not found",
        )

    if exercise_log.completed and exercise_log.skipped:
        raise HTTPException(
            status_code=400,
            detail="Exercise cannot be both completed and skipped.",
        )

    new_log = ExerciseLog(**exercise_log.model_dump())

    db.add(new_log)
    db.commit()
    db.refresh(new_log)

    return new_log


# Get all exercise logs
@router.get("/", response_model=list[ExerciseLogResponse])
def get_exercise_logs(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return (
        db.query(ExerciseLog)
        .join(WorkoutSession)
        .filter(
            WorkoutSession.user_id == current_user.id
        )
        .order_by(
            ExerciseLog.workout_session_id,
            ExerciseLog.order,
        )
        .all()
    )


# Get one exercise log
@router.get("/{exercise_log_id}", response_model=ExerciseLogResponse)
def get_exercise_log(
    exercise_log_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    exercise_log = (
        db.query(ExerciseLog)
        .join(WorkoutSession)
        .filter(
            ExerciseLog.id == exercise_log_id,
            WorkoutSession.user_id == current_user.id,
        )
        .first()
    )

    if not exercise_log:
        raise HTTPException(
            status_code=404,
            detail="Exercise log not found",
        )

    return exercise_log


# Update exercise log
@router.put("/{exercise_log_id}", response_model=ExerciseLogResponse)
def update_exercise_log(
    exercise_log_id: int,
    exercise_log_update: ExerciseLogUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    exercise_log = (
        db.query(ExerciseLog)
        .join(WorkoutSession)
        .filter(
            ExerciseLog.id == exercise_log_id,
            WorkoutSession.user_id == current_user.id,
        )
        .first()
    )

    if not exercise_log:
        raise HTTPException(
            status_code=404,
            detail="Exercise log not found",
        )

    update_data = exercise_log_update.model_dump(exclude_unset=True)

    if (
        update_data.get("completed", exercise_log.completed)
        and update_data.get("skipped", exercise_log.skipped)
    ):
        raise HTTPException(
            status_code=400,
            detail="Exercise cannot be both completed and skipped.",
        )

    for key, value in update_data.items():
        setattr(exercise_log, key, value)

    db.commit()
    db.refresh(exercise_log)

    return exercise_log


# Delete exercise log
@router.delete(
    "/{exercise_log_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_exercise_log(
    exercise_log_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    exercise_log = (
        db.query(ExerciseLog)
        .join(WorkoutSession)
        .filter(
            ExerciseLog.id == exercise_log_id,
            WorkoutSession.user_id == current_user.id,
        )
        .first()
    )

    if not exercise_log:
        raise HTTPException(
            status_code=404,
            detail="Exercise log not found",
        )

    db.delete(exercise_log)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)