from datetime import date

import strawberry
from typing import List
from strawberry import Info
from app.ms_coaches_sportsmen.models import Coach
from app.ms_sections.models import SportSection
from app.ms_sport.types import SportType
from app.ms_coaches_sportsmen.types import SportsmanType, CoachType


@strawberry.type
class SportSectionType:
    id: int
    title: str
    sport: SportType
    description: str
    capacity: int
    sportsmen: List[SportsmanType]


@strawberry.type
class SportSectionCoachType:
    id: int
    coach: CoachType
    section: SportSectionType
    start: date
    end: date | None

    @strawberry.field()
    def get_section(self, info=Info) -> SportSectionType:
        db = info.context["db"]
        section_id = self.section
        section_obj = db.query(SportSection).filter(SportSection.id == section_id).first()
        return section_obj

    @strawberry.field()
    def get_coach(self, info=Info) -> CoachType:
        db = info.context["db"]
        coach_obj = db.query(Coach).filter(Coach.id == self.coach).first()
        return coach_obj
