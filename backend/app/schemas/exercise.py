from typing import Optional
from pydantic import BaseModel


class ExerciseBase(BaseModel):
    name: str
    target_sets: int
    target_reps: str
    rest_time_seconds: Optional[int] = None
    notes: Optional[str] = None
    order: int


class ExerciseCreate(ExerciseBase):
    workout_day_id: int


class ExerciseUpdate(BaseModel):
    name: Optional[str] = None
    target_sets: Optional[int] = None
    target_reps: Optional[str] = None
    rest_time_seconds: Optional[int] = None
    notes: Optional[str] = None
    order: Optional[int] = None


class ExerciseResponse(ExerciseBase):
    id: int
    workout_day_id: int

    class Config:
        from_attributes = True