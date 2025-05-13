from sqlalchemy import Column, Integer, String, Date
from app.database import Base
from sqlalchemy import Table, ForeignKey
from sqlalchemy.orm import relationship


section_sportsman_association = Table(
    "section_sportsman_association",
    Base.metadata,
    Column("sport_section_id", Integer, ForeignKey("sport_sections.id"), primary_key=True),
    Column("sportsman_id", Integer, ForeignKey("sportsmen.id"), primary_key=True)
)


class SportSection(Base):
    __tablename__ = "sport_sections"

    id = Column(Integer, primary_key=True)
    title = Column(String(50), nullable=False)
    sport_id = Column(Integer, ForeignKey("sports.id"), nullable=False)
    description = Column(String(100), nullable=False)
    capacity = Column(Integer, nullable=False)
    sportsmen = relationship("Sportsman", secondary=section_sportsman_association, back_populates="sections")
    sport = relationship("Sport")


class SportSectionCoach(Base):
    __tablename__ = "sport_section_coaches"

    id = Column(Integer, primary_key=True)
    coach_id = Column(Integer, ForeignKey("coaches.id"), nullable=False)
    section_id = Column(Integer, ForeignKey("sport_sections.id"), nullable=False)
    start = Column(Date, nullable=False)
    end = Column(Date, nullable=True)
