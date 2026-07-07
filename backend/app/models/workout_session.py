from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from app.core.database import Base


class WorkoutSession(Base):
    __tablename__ = "workout_sessions"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    workout_plan_id = Column(
        Integer,
        ForeignKey("workout_plans.id", ondelete="CASCADE"),
        nullable=False,
    )

    started_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    ended_at = Column(
        DateTime,
        nullable=True,
    )

    status = Column(
        String,
        default="IN_PROGRESS",
        nullable=False,
    )

    notes = Column(
        String,
        nullable=True,
    )

    user = relationship(
        "User",
        back_populates="workout_sessions",
    )

    workout_plan = relationship(
        "WorkoutPlan",
        back_populates="workout_sessions",
    )
    
    exercise_logs = relationship(
    "ExerciseLog",
    back_populates="workout_session",
    cascade="all, delete-orphan",
)