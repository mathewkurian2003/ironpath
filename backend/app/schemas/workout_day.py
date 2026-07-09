from typing import List, Optional

from pydantic import BaseModel

from .workout_day_exercise import WorkoutDayExerciseResponse


class WorkoutDayBase(BaseModel):
    name: str
    day_of_week: str
    order: int


class WorkoutDayCreate(WorkoutDayBase):
    workout_plan_id: int


class WorkoutDayUpdate(BaseModel):
    name: Optional[str] = None
    day_of_week: Optional[str] = None
    order: Optional[int] = None


class WorkoutDayResponse(WorkoutDayBase):
    id: int
    workout_plan_id: int

    # NEW
    workout_day_exercises: List[WorkoutDayExerciseResponse] = []

    class Config:
        from_attributes = True