from pydantic import BaseModel
from typing import Optional


class ExerciseLogBase(BaseModel):
    workout_session_id: int
    exercise_id: int
    order: int


class ExerciseLogCreate(ExerciseLogBase):
    pass


class ExerciseLogUpdate(BaseModel):
    order: Optional[int] = None


class ExerciseLogResponse(ExerciseLogBase):
    id: int

    class Config:
        from_attributes = True