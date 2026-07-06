from sqlalchemy import Column, Integer, Float, String, ForeignKey
from sqlalchemy.orm import relationship

from app.core.database import Base


class Profile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True, index=True)

    age = Column(Integer)
    height = Column(Float)
    weight = Column(Float)

    gender = Column(String(20))
    fitness_goal = Column(String(100))
    experience_level = Column(String(50))
    activity_level = Column(String(50))

    user_id = Column(Integer, ForeignKey("users.id"), unique=True)

    user = relationship("User", back_populates="profile")