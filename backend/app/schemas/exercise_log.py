from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ExerciseLogBase(BaseModel):
    workout_session_id: int
    exercise_id: int
    order: int

    planned_sets: int
    planned_reps: int
    planned_weight: float

    completed: bool = False
    skipped: bool = False
    notes: Optional[str] = None


class ExerciseLogCreate(ExerciseLogBase):
    pass


class ExerciseLogUpdate(BaseModel):
    order: Optional[int] = None

    planned_sets: Optional[int] = None
    planned_reps: Optional[int] = None
    planned_weight: Optional[float] = None

    completed: Optional[bool] = None
    skipped: Optional[bool] = None

    notes: Optional[str] = None


class ExerciseLogResponse(ExerciseLogBase):
    id: int

    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True