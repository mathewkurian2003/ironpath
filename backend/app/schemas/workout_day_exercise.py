from typing import Optional

from pydantic import BaseModel


class WorkoutDayExerciseBase(BaseModel):
    exercise_id: int
    order: int
    target_sets: int
    target_reps: str
    target_weight: Optional[int] = None
    rest_time_seconds: Optional[int] = None
    notes: Optional[str] = None


class WorkoutDayExerciseCreate(WorkoutDayExerciseBase):
    pass


class WorkoutDayExerciseUpdate(BaseModel):
    exercise_id: Optional[int] = None
    order: Optional[int] = None
    target_sets: Optional[int] = None
    target_reps: Optional[str] = None
    target_weight: Optional[int] = None
    rest_time_seconds: Optional[int] = None
    notes: Optional[str] = None


class WorkoutDayExerciseResponse(WorkoutDayExerciseBase):
    id: int
    workout_day_id: int

    class Config:
        from_attributes = True