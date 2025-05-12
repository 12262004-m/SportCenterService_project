from sqlalchemy import Column, Integer, String, Enum
from app.database import Base
from enum import Enum as PyEnum

class SportTypeEnum(PyEnum):
    TEAM = "TEAM"
    INDIVIDUAL = "INDIVIDUAL"

class Sport(Base):
    __tablename__ = "sports"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False, unique=True)
    type = Column(Enum(SportTypeEnum), nullable=False)

