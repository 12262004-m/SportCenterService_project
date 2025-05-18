from app.database import Base
from sqlalchemy import Column, Integer, ForeignKey, Enum, Time
from enum import Enum as PyEnum


class WeekdayEnum(PyEnum):
    MONDAY = "MONDAY"
    TUESDAY = "TUESDAY"
    WEDNESDAY = "WEDNESDAY"
    THURSDAY = "THURSDAY"
    FRIDAY = "FRIDAY"
    SATURDAY = "SATURDAY"
    SUNDAY = "SUNDAY"


class Schedule(Base):
    __tablename__ = "schedule"

    id = Column(Integer, primary_key=True, index=True)
    section_id = Column(Integer, ForeignKey("sport_sections.id"), nullable=False)
    hall_id = Column(Integer, ForeignKey("sport_halls.id"), nullable=False)
    weekday = Column(Enum(WeekdayEnum), nullable=False)
    start = Column(Time, nullable=False)
    end = Column(Time, nullable=True)
