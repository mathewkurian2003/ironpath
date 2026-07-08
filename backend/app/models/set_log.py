from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class SetLog(Base):
    __tablename__ = "set_logs"

    id = Column(Integer, primary_key=True, index=True)

    exercise_log_id = Column(
        Integer,
        ForeignKey("exercise_logs.id", ondelete="CASCADE"),
        nullable=False,
    )

    set_number = Column(Integer, nullable=False)

    planned_weight = Column(Float, nullable=True)
    actual_weight = Column(Float, nullable=True)

    planned_reps = Column(Integer, nullable=True)
    actual_reps = Column(Integer, nullable=True)

    rpe = Column(Float, nullable=True)
    rir = Column(Integer, nullable=True)

    completed = Column(Boolean, default=False)
    notes = Column(Text, nullable=True)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    exercise_log = relationship(
        "ExerciseLog",
        back_populates="set_logs",
    )