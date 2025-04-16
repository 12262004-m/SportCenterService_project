from sqlalchemy import Column, Integer, String, Date, Enum
from sqlalchemy.ext.declarative import declarative_base
from enum import Enum as PyEnum

Base = declarative_base()


class GenderEnum(PyEnum):
    MALE = "MALE"
    FEMALE = "FEMALE"


class Coach(Base):
    __tablename__ = "coaches"

    id = Column(Integer, primary_key=True, index=True)
    last_name = Column(String, index=True)
    first_name = Column(String)
    middle_name = Column(String)
    gender = Column(Enum(GenderEnum), nullable=False, index=True)  # Используем Enum с Python Enum
    date_of_birth = Column(Date)
    qualification = Column(String)
    experience = Column(Integer)



class Sportsman(Base):
    __tablename__ = "sportsmen"

    id = Column(Integer, primary_key=True, index=True)
    last_name = Column(String, index=True)
    first_name = Column(String)
    middle_name = Column(String)
    gender = Column(Enum(GenderEnum), nullable=False, index=True)
    date_of_birth = Column(Date)
    phone_number = Column(String(11))
    email = Column(String, index=True)
    registration_date = Column(Date)
