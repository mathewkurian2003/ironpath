from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship


from app.core.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    roadmaps = relationship(
    "Roadmap",
    back_populates="owner",
    cascade="all, delete-orphan"
)
    profile = relationship(
    "Profile",
    back_populates="user",
    uselist=False,
    cascade="all, delete"
)
    workout_plans = relationship(
    "WorkoutPlan",
    back_populates="owner",
    cascade="all, delete-orphan"
)