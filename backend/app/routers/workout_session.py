from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.core.database import get_db

from app.models.user import User
from app.models.workout_plan import WorkoutPlan
from app.models.workout_session import WorkoutSession

from app.schemas.workout_session import (
    WorkoutSessionCreate,
    WorkoutSessionUpdate,
    WorkoutSessionResponse,
)

router = APIRouter(
    prefix="/workout-sessions",
    tags=["Workout Sessions"],
)


# Start a workout session
@router.post("/", response_model=WorkoutSessionResponse)
def create_workout_session(
    workout_session: WorkoutSessionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    workout_plan = (
        db.query(WorkoutPlan)
        .filter(
            WorkoutPlan.id == workout_session.workout_plan_id,
            WorkoutPlan.owner_id == current_user.id,
        )
        .first()
    )

    if not workout_plan:
        raise HTTPException(
            status_code=404,
            detail="Workout plan not found",
        )

    session = WorkoutSession(
        user_id=current_user.id,
        workout_plan_id=workout_session.workout_plan_id,
        notes=workout_session.notes,
    )

    db.add(session)
    db.commit()
    db.refresh(session)

    return session


# Get all workout sessions
@router.get("/", response_model=list[WorkoutSessionResponse])
def get_workout_sessions(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return (
        db.query(WorkoutSession)
        .filter(WorkoutSession.user_id == current_user.id)
        .order_by(WorkoutSession.started_at.desc())
        .all()
    )


# Get one workout session
@router.get("/{session_id}", response_model=WorkoutSessionResponse)
def get_workout_session(
    session_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    session = (
        db.query(WorkoutSession)
        .filter(
            WorkoutSession.id == session_id,
            WorkoutSession.user_id == current_user.id,
        )
        .first()
    )

    if not session:
        raise HTTPException(
            status_code=404,
            detail="Workout session not found",
        )

    return session


# Complete a workout session
@router.post("/{session_id}/complete", response_model=WorkoutSessionResponse)
def complete_workout_session(
    session_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    session = (
        db.query(WorkoutSession)
        .filter(
            WorkoutSession.id == session_id,
            WorkoutSession.user_id == current_user.id,
        )
        .first()
    )

    if not session:
        raise HTTPException(
            status_code=404,
            detail="Workout session not found",
        )

    session.ended_at = datetime.utcnow()
    session.status = "COMPLETED"

    db.commit()
    db.refresh(session)

    return session


# Update workout session
@router.put("/{session_id}", response_model=WorkoutSessionResponse)
def update_workout_session(
    session_id: int,
    workout_session: WorkoutSessionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    session = (
        db.query(WorkoutSession)
        .filter(
            WorkoutSession.id == session_id,
            WorkoutSession.user_id == current_user.id,
        )
        .first()
    )

    if not session:
        raise HTTPException(
            status_code=404,
            detail="Workout session not found",
        )

    update_data = workout_session.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(session, key, value)

    db.commit()
    db.refresh(session)

    return session


# Delete workout session
@router.delete("/{session_id}")
def delete_workout_session(
    session_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    session = (
        db.query(WorkoutSession)
        .filter(
            WorkoutSession.id == session_id,
            WorkoutSession.user_id == current_user.id,
        )
        .first()
    )

    if not session:
        raise HTTPException(
            status_code=404,
            detail="Workout session not found",
        )

    db.delete(session)
    db.commit()

    return {
        "message": "Workout session deleted successfully"
    }