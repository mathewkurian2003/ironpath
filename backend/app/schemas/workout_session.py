from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class WorkoutSessionBase(BaseModel):
    workout_plan_id: int
    notes: Optional[str] = None


class WorkoutSessionCreate(WorkoutSessionBase):
    pass


class WorkoutSessionUpdate(BaseModel):
    ended_at: Optional[datetime] = None
    status: Optional[str] = None
    notes: Optional[str] = None


class WorkoutSessionResponse(BaseModel):
    id: int
    user_id: int
    workout_plan_id: int
    started_at: datetime
    ended_at: Optional[datetime] = None
    status: str
    notes: Optional[str] = None

    class Config:
        from_attributes = True