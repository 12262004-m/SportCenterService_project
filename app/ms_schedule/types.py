from datetime import time
import strawberry
from app.ms_schedule.enums import GraphQLWeekdayEnum
from app.ms_sections.types import SportSectionType
from app.ms_sport.types import SportHallType


@strawberry.type
class ScheduleType:
    id: int
    section: SportSectionType
    hall: SportHallType
    weekday: GraphQLWeekdayEnum
    start: time
    end: time
