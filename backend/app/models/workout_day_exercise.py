from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import relationship

from app.core.database import Base


class WorkoutDayExercise(Base):
    __tablename__ = "workout_day_exercises"

    id = Column(Integer, primary_key=True, index=True)

    workout_day_id = Column(
        Integer,
        ForeignKey("workout_days.id", ondelete="CASCADE"),
        nullable=False,
    )

    exercise_id = Column(
        Integer,
        ForeignKey("exercises.id", ondelete="CASCADE"),
        nullable=False,
    )

    order = Column(Integer, nullable=False)

    target_sets = Column(Integer, nullable=False)

    target_reps = Column(String, nullable=False)

    target_weight = Column(Integer, nullable=True)

    rest_time_seconds = Column(Integer, nullable=True)

    notes = Column(String, nullable=True)

    workout_day = relationship(
        "WorkoutDay",
        back_populates="workout_day_exercises",
    )

    exercise = relationship(
        "Exercise",
        back_populates="workout_day_exercises",
    )

    exercise_logs = relationship(
        "ExerciseLog",
        back_populates="workout_day_exercise",
        cascade="all, delete-orphan",
    )