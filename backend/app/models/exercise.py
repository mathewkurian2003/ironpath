from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    Text,
    JSON,
)
from sqlalchemy.orm import relationship

from app.core.database import Base


class Exercise(Base):
    __tablename__ = "exercises"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False, unique=True)
    slug = Column(String, unique=True, nullable=False)

    primary_muscle = Column(String, nullable=False)
    secondary_muscles = Column(JSON, nullable=True)

    equipment = Column(String, nullable=True)
    exercise_type = Column(String, nullable=True)

    movement_pattern = Column(String, nullable=True)

    difficulty = Column(String, nullable=True)

    mechanic = Column(String, nullable=True)

    force_type = Column(String, nullable=True)

    instructions = Column(Text, nullable=True)
    tips = Column(Text, nullable=True)

    video_url = Column(String, nullable=True)
    image_url = Column(String, nullable=True)

    is_compound = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)

    workout_day_exercises = relationship(
        "WorkoutDayExercise",
        back_populates="exercise",
    )

    exercise_logs = relationship(
        "ExerciseLog",
        back_populates="exercise",
    )