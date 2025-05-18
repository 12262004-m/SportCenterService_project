import strawberry
import datetime
from strawberry.types import Info
from app.ms_schedule import crud
from app.ms_schedule.enums import GraphQLWeekdayEnum
from app.ms_schedule.models import Schedule
from app.ms_schedule.types import ScheduleType
import time


@strawberry.type
class ScheduleMutation:
    @strawberry.mutation()
    def create_schedule(
            self,
            info: Info,
            section_id: int,
            hall_id: int,
            weekday: GraphQLWeekdayEnum,
            start: datetime.time,
            end: datetime.time
    ) -> ScheduleType:
        db = info.context["db"]
        schedule_data = {
            "section_id": section_id,
            "hall_id": hall_id,
            "weekday": weekday,
            "start": start,
            "end": end
        }
        schedule = crud.create_schedule(db, schedule_data)
        return ScheduleType(
            id=schedule.id,
            section=schedule.section_id,
            hall=schedule.hall_id,
            weekday=schedule.weekday,
            start=schedule.start,
            end=schedule.end,
        )


