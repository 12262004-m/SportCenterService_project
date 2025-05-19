from sqlalchemy import Column, Integer, String, Enum
from app.database import Base
from enum import Enum as PyEnum
from sqlalchemy import Table, ForeignKey
from sqlalchemy.orm import relationship


hall_sport_association = Table(
    "hall_sport_association",
    Base.metadata,
    Column("sporthall_id", Integer, ForeignKey("sport_halls.id")),
    Column("sport_id", Integer, ForeignKey("sports.id"))
)


class SportTypeEnum(PyEnum):
    TEAM = "TEAM"
    INDIVIDUAL = "INDIVIDUAL"


class Sport(Base):
    __tablename__ = "sports"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False, unique=True)
    type = Column(Enum(SportTypeEnum), nullable=False)


class SportHall(Base):
    __tablename__ = "sport_halls"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    address = Column(String(50), nullable=False)
    sports = relationship("Sport", secondary=hall_sport_association, backref="sport_halls")
