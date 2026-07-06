from pydantic import BaseModel
from typing import Optional


class ProfileBase(BaseModel):
    age: int
    height: float
    weight: float
    gender: str
    fitness_goal: str
    experience_level: str
    activity_level: str


class ProfileCreate(ProfileBase):
    pass


class ProfileResponse(ProfileBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True