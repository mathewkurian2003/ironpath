from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.core.database import get_db

from app.models.user import User
from app.models.set_log import SetLog
from app.models.exercise_log import ExerciseLog
from app.models.workout_session import WorkoutSession

from app.schemas.set_log import (
    SetLogCreate,
    SetLogUpdate,
    SetLogResponse,
)

router = APIRouter(
    prefix="/set-logs",
    tags=["Set Logs"],
)


@router.post("/", response_model=SetLogResponse)
def create_set_log(
    set_log: SetLogCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    exercise_log = (
        db.query(ExerciseLog)
        .join(WorkoutSession)
        .filter(
            ExerciseLog.id == set_log.exercise_log_id,
            WorkoutSession.user_id == current_user.id,
        )
        .first()
    )

    if not exercise_log:
        raise HTTPException(
            status_code=404,
            detail="Exercise log not found",
        )

    new_set_log = SetLog(**set_log.model_dump())

    db.add(new_set_log)
    db.commit()
    db.refresh(new_set_log)

    return new_set_log


@router.get("/", response_model=list[SetLogResponse])
def get_set_logs(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return (
        db.query(SetLog)
        .join(ExerciseLog)
        .join(WorkoutSession)
        .filter(WorkoutSession.user_id == current_user.id)
        .order_by(
            ExerciseLog.id,
            SetLog.set_number,
        )
        .all()
    )


@router.get("/{set_log_id}", response_model=SetLogResponse)
def get_set_log(
    set_log_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    set_log = (
        db.query(SetLog)
        .join(ExerciseLog)
        .join(WorkoutSession)
        .filter(
            SetLog.id == set_log_id,
            WorkoutSession.user_id == current_user.id,
        )
        .first()
    )

    if not set_log:
        raise HTTPException(
            status_code=404,
            detail="Set log not found",
        )

    return set_log


@router.put("/{set_log_id}", response_model=SetLogResponse)
def update_set_log(
    set_log_id: int,
    set_log_update: SetLogUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    set_log = (
        db.query(SetLog)
        .join(ExerciseLog)
        .join(WorkoutSession)
        .filter(
            SetLog.id == set_log_id,
            WorkoutSession.user_id == current_user.id,
        )
        .first()
    )

    if not set_log:
        raise HTTPException(
            status_code=404,
            detail="Set log not found",
        )

    update_data = set_log_update.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(set_log, key, value)

    db.commit()
    db.refresh(set_log)

    return set_log


@router.delete(
    "/{set_log_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_set_log(
    set_log_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    set_log = (
        db.query(SetLog)
        .join(ExerciseLog)
        .join(WorkoutSession)
        .filter(
            SetLog.id == set_log_id,
            WorkoutSession.user_id == current_user.id,
        )
        .first()
    )

    if not set_log:
        raise HTTPException(
            status_code=404,
            detail="Set log not found",
        )

    db.delete(set_log)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)