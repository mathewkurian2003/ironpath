from typing import List

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.auth.dependencies import get_current_user
from app.models import ExerciseLog, SetLog, User
from app.schemas import SetLogCreate, SetLogResponse, SetLogUpdate

router = APIRouter(
    prefix="/set-logs",
    tags=["Set Logs"],
)


@router.post(
    "/",
    response_model=SetLogResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_set_log(
    set_log: SetLogCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    exercise_log = (
        db.query(ExerciseLog)
        .filter(ExerciseLog.id == set_log.exercise_log_id)
        .first()
    )

    if not exercise_log:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Exercise log not found",
        )

    db_set_log = SetLog(**set_log.model_dump())

    db.add(db_set_log)
    db.commit()
    db.refresh(db_set_log)

    return db_set_log


@router.get(
    "/",
    response_model=List[SetLogResponse],
)
def get_set_logs(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return (
        db.query(SetLog)
        .order_by(SetLog.id)
        .all()
    )


@router.get(
    "/{set_log_id}",
    response_model=SetLogResponse,
)
def get_set_log(
    set_log_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    set_log = (
        db.query(SetLog)
        .filter(SetLog.id == set_log_id)
        .first()
    )

    if not set_log:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Set log not found",
        )

    return set_log


@router.put(
    "/{set_log_id}",
    response_model=SetLogResponse,
)
def update_set_log(
    set_log_id: int,
    update: SetLogUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    set_log = (
        db.query(SetLog)
        .filter(SetLog.id == set_log_id)
        .first()
    )

    if not set_log:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Set log not found",
        )

    for key, value in update.model_dump(exclude_unset=True).items():
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
        .filter(SetLog.id == set_log_id)
        .first()
    )

    if not set_log:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Set log not found",
        )

    db.delete(set_log)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)