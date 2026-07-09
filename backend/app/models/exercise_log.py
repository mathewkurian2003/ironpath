from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    Text,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class ExerciseLog(Base):
    __tablename__ = "exercise_logs"

    id = Column(Integer, primary_key=True, index=True)

    workout_session_id = Column(
        Integer,
        ForeignKey("workout_sessions.id", ondelete="CASCADE"),
        nullable=False,
    )

    # Reference to the programmed exercise in the workout day
    workout_day_exercise_id = Column(
        Integer,
        ForeignKey("workout_day_exercises.id", ondelete="CASCADE"),
        nullable=False,
    )

    # Order of exercise in the workout
    order = Column(Integer, nullable=False)

    # Planned workout target
    planned_sets = Column(Integer, nullable=False)
    planned_reps = Column(Integer, nullable=False)
    planned_weight = Column(Float, nullable=False)

    # Exercise status
    completed = Column(Boolean, default=False, nullable=False)
    skipped = Column(Boolean, default=False, nullable=False)

    # User notes
    notes = Column(Text, nullable=True)

    # Audit fields
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    # Relationships
    workout_session = relationship(
        "WorkoutSession",
        back_populates="exercise_logs",
    )

    workout_day_exercise = relationship(
        "WorkoutDayExercise",
        back_populates="exercise_logs",
    )

    set_logs = relationship(
        "SetLog",
        back_populates="exercise_log",
        cascade="all, delete-orphan",
    )