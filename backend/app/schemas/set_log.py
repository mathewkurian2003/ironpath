from typing import Optional

from pydantic import BaseModel, ConfigDict


class SetLogBase(BaseModel):
    set_number: int
    weight: float
    reps: int
    rir: Optional[float] = None
    rpe: Optional[float] = None
    duration_seconds: Optional[int] = None
    completed: bool = True
    failed: bool = False
    notes: Optional[str] = None


class SetLogCreate(SetLogBase):
    exercise_log_id: int


class SetLogUpdate(BaseModel):
    weight: Optional[float] = None
    reps: Optional[int] = None
    rir: Optional[float] = None
    rpe: Optional[float] = None
    duration_seconds: Optional[int] = None
    completed: Optional[bool] = None
    failed: Optional[bool] = None
    notes: Optional[str] = None


class SetLogResponse(SetLogBase):
    id: int
    exercise_log_id: int

    model_config = ConfigDict(from_attributes=True)