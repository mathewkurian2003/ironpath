from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.core.database import Base


class WorkoutDay(Base):
    __tablename__ = "workout_days"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)          # Push, Pull, Legs
    day_of_week = Column(String, nullable=False)   # Monday, Tuesday
    order = Column(Integer, nullable=False)

    workout_plan_id = Column(
        Integer,
        ForeignKey("workout_plans.id", ondelete="CASCADE"),
        nullable=False
    )

    workout_plan = relationship(
        "WorkoutPlan",
        back_populates="workout_days"
    )

    workout_day_exercises = relationship(
    "WorkoutDayExercise",
    back_populates="workout_day",
    cascade="all, delete-orphan",
)
    workout_sessions = relationship(
    "WorkoutSession",
    back_populates="workout_day",
    cascade="all, delete-orphan",
)