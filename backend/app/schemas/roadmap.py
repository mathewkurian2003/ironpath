from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel


class RoadmapBase(BaseModel):
    title: str
    description: Optional[str] = None
    target_date: Optional[date] = None


class RoadmapCreate(RoadmapBase):
    pass


class RoadmapUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    target_date: Optional[date] = None
    status: Optional[str] = None
    progress: Optional[int] = None


class RoadmapResponse(RoadmapBase):
    id: int
    status: str
    progress: int
    owner_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True