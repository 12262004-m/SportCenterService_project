import strawberry
from typing import List
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
    start: str
    end: str | None
