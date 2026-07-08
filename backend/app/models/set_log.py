from sqlalchemy import (
    Column,
    Integer,
    Float,
    Boolean,
    ForeignKey,
    Text
)
from sqlalchemy.orm import relationship

from app.core.database import Base


class SetLog(Base):
    __tablename__ = "set_logs"

    id = Column(Integer, primary_key=True, index=True)

    exercise_log_id = Column(
        Integer,
        ForeignKey("exercise_logs.id", ondelete="CASCADE"),
        nullable=False
    )

    set_number = Column(Integer, nullable=False)

    weight = Column(Float, nullable=False)

    reps = Column(Integer, nullable=False)

    rir = Column(Float, nullable=True)

    rpe = Column(Float, nullable=True)

    duration_seconds = Column(Integer, nullable=True)

    completed = Column(Boolean, default=True)

    failed = Column(Boolean, default=False)

    notes = Column(Text, nullable=True)

    exercise_log = relationship(
        "ExerciseLog",
        back_populates="set_logs"
    )