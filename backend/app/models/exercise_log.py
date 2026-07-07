from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from app.core.database import Base


class ExerciseLog(Base):
    __tablename__ = "exercise_logs"

    id = Column(Integer, primary_key=True, index=True)

    workout_session_id = Column(
        Integer,
        ForeignKey("workout_sessions.id", ondelete="CASCADE"),
        nullable=False,
    )

    exercise_id = Column(
        Integer,
        ForeignKey("exercises.id", ondelete="CASCADE"),
        nullable=False,
    )

    order = Column(
        Integer,
        nullable=False,
    )

    workout_session = relationship(
        "WorkoutSession",
        back_populates="exercise_logs",
    )

    exercise = relationship(
        "Exercise",
        back_populates="exercise_logs",
    )