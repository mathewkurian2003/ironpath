from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class SetLogBase(BaseModel):
    exercise_log_id: int
    set_number: int

    planned_weight: Optional[float] = None
    actual_weight: Optional[float] = None

    planned_reps: Optional[int] = None
    actual_reps: Optional[int] = None

    rpe: Optional[float] = None
    rir: Optional[int] = None

    completed: bool = False
    notes: Optional[str] = None


class SetLogCreate(SetLogBase):
    pass


class SetLogUpdate(BaseModel):
    planned_weight: Optional[float] = None
    actual_weight: Optional[float] = None

    planned_reps: Optional[int] = None
    actual_reps: Optional[int] = None

    rpe: Optional[float] = None
    rir: Optional[int] = None

    completed: Optional[bool] = None
    notes: Optional[str] = None


class SetLogResponse(SetLogBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True