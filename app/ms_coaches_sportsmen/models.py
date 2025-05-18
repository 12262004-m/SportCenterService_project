from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import relationship
from app.database import Base
from app.ms_sections.models import section_sportsman_association


class Coach(Base):
    __tablename__ = "coaches"

    id = Column(Integer, primary_key=True, index=True)
    last_name = Column(String, index=True)
    first_name = Column(String)
    middle_name = Column(String)
    gender = Column(String, nullable=False)
    date_of_birth = Column(Date)
    qualification = Column(String)
    experience = Column(Integer)


class Sportsman(Base):
    __tablename__ = "sportsmen"

    id = Column(Integer, primary_key=True, index=True)
    last_name = Column(String, index=True)
    first_name = Column(String)
    middle_name = Column(String)
    gender = Column(String, nullable=False)
    date_of_birth = Column(Date)
    phone_number = Column(String(11))
    email = Column(String, index=True)
    registration_date = Column(Date)
    sections = relationship("SportSection", secondary=section_sportsman_association, back_populates="sportsmen")
