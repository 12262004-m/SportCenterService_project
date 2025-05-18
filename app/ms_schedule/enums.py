import strawberry
from app.ms_schedule.models import WeekdayEnum

GraphQLWeekdayEnum = strawberry.enum(WeekdayEnum, name="WeekdayEnum")
