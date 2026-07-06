from typing import Optional
from pydantic import BaseModel


class WorkoutPlanBase(BaseModel):
    name: str
    description: Optional[str] = None


class WorkoutPlanCreate(WorkoutPlanBase):
    pass


# ADD THIS
class WorkoutPlanUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


class WorkoutPlanResponse(WorkoutPlanBase):
    id: int
    owner_id: int

    class Config:
        from_attributes = True