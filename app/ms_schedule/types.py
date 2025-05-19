from datetime import time
import strawberry
from strawberry.types import Info
from app.ms_coaches_sportsmen.types import CoachType
from app.ms_schedule.enums import GraphQLWeekdayEnum
from app.ms_sections.types import SportSectionType
from app.ms_sport.types import SportHallType
from app.ms_sport.models import SportHall
from app.ms_sections.models import SportSection, SportSectionCoach
from app.ms_coaches_sportsmen.models import Coach


@strawberry.type
class ScheduleType:
    id: int
    section: SportSectionType
    hall: SportHallType
    weekday: GraphQLWeekdayEnum
    start: time
    end: time

    @strawberry.field()
    def get_hall(self, info=Info) -> SportHallType:
        db = info.context["db"]
        hall_id = self.hall
        hall_obj = db.query(SportHall).filter(SportHall.id == hall_id).first()
        return hall_obj

    @strawberry.field()
    def get_section(self, info=Info) -> SportSectionType:
        db = info.context["db"]
        section_id = self.section
        section_obj = db.query(SportSection).filter(SportSection.id == section_id).first()
        return section_obj

    @strawberry.field()
    def get_coach(self, info=Info) -> CoachType:
        db = info.context["db"]
        section_id = self.section
        obj = db.query(SportSectionCoach).filter(SportSectionCoach.section_id == section_id).first()
        coach_obj = db.query(Coach).filter(Coach.id == obj.coach_id).first()
        return coach_obj
