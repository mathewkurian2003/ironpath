from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.core.database import Base


class Exercise(Base):
    __tablename__ = "exercises"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)

    target_sets = Column(Integer, nullable=False)

    target_reps = Column(String, nullable=False)
    # Examples:
    # "8-10"
    # "12"
    # "AMRAP"

    rest_time_seconds = Column(Integer, nullable=True)

    notes = Column(String, nullable=True)

    order = Column(Integer, nullable=False)

    workout_day_id = Column(
        Integer,
        ForeignKey("workout_days.id", ondelete="CASCADE"),
        nullable=False
    )

    workout_day = relationship(
        "WorkoutDay",
        back_populates="exercises"
    )

    exercise_logs = relationship(
    "ExerciseLog",
    back_populates="exercise",
    cascade="all, delete-orphan",
)