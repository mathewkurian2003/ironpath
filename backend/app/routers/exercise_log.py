from fastapi import APIRouter, Depends, HTTPException
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
    session = (
        db.query(WorkoutSession)
        .filter(
            WorkoutSession.id == exercise_log.workout_session_id,
            WorkoutSession.user_id == current_user.id,
        )
        .first()
    )

    if not session:
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

    new_log = ExerciseLog(
        workout_session_id=exercise_log.workout_session_id,
        exercise_id=exercise_log.exercise_id,
        order=exercise_log.order,
    )

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
        .filter(WorkoutSession.user_id == current_user.id)
        .order_by(ExerciseLog.order)
        .all()
    )


# Get one exercise log
@router.get("/{log_id}", response_model=ExerciseLogResponse)
def get_exercise_log(
    log_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    log = (
        db.query(ExerciseLog)
        .join(WorkoutSession)
        .filter(
            ExerciseLog.id == log_id,
            WorkoutSession.user_id == current_user.id,
        )
        .first()
    )

    if not log:
        raise HTTPException(
            status_code=404,
            detail="Exercise log not found",
        )

    return log


# Update exercise log
@router.put("/{log_id}", response_model=ExerciseLogResponse)
def update_exercise_log(
    log_id: int,
    exercise_log: ExerciseLogUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    log = (
        db.query(ExerciseLog)
        .join(WorkoutSession)
        .filter(
            ExerciseLog.id == log_id,
            WorkoutSession.user_id == current_user.id,
        )
        .first()
    )

    if not log:
        raise HTTPException(
            status_code=404,
            detail="Exercise log not found",
        )

    update_data = exercise_log.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(log, key, value)

    db.commit()
    db.refresh(log)

    return log


# Delete exercise log
@router.delete("/{log_id}")
def delete_exercise_log(
    log_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    log = (
        db.query(ExerciseLog)
        .join(WorkoutSession)
        .filter(
            ExerciseLog.id == log_id,
            WorkoutSession.user_id == current_user.id,
        )
        .first()
    )

    if not log:
        raise HTTPException(
            status_code=404,
            detail="Exercise log not found",
        )

    db.delete(log)
    db.commit()

    return {
        "message": "Exercise log deleted successfully"
    }