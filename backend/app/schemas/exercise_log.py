from datetime import datetime
from typing import Optional

from pydantic import BaseModel


# Used when creating an exercise log.
# The backend will automatically copy the planned values
# from WorkoutDayExercise.
class ExerciseLogCreate(BaseModel):
    workout_session_id: int
    workout_day_exercise_id: int


class ExerciseLogUpdate(BaseModel):
    completed: Optional[bool] = None
    skipped: Optional[bool] = None

    planned_sets: Optional[int] = None
    planned_reps: Optional[int] = None
    planned_weight: Optional[float] = None

    notes: Optional[str] = None


class ExerciseLogResponse(BaseModel):
    id: int

    workout_session_id: int
    workout_day_exercise_id: int

    order: int

    planned_sets: int
    planned_reps: str
    planned_weight: float

    completed: bool
    skipped: bool

    notes: Optional[str] = None

    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True