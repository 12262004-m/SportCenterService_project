import strawberry
from app.ms_coaches_sportsmen.schema import CoachSportsmenMutation, CoachSportsmenQuery
from app.ms_auth.schema import UserMutation, UserQuery
from app.ms_sport.schema import SportMutation, SportHallMutation, SportQuery, SportHallQuery
from app.ms_sections.schema import SportSectionQuery, SportSectionMutation, SportSectionCoachesQuery, SportSectionCoachesMutation
from app.ms_schedule.schema import ScheduleMutation, ScheduleQuery


@strawberry.type
class Query(CoachSportsmenQuery, UserQuery, SportQuery, SportHallQuery, SportSectionQuery, SportSectionCoachesQuery, ScheduleQuery):
    pass


@strawberry.type
class Mutation(CoachSportsmenMutation, UserMutation, SportMutation, SportHallMutation, SportSectionMutation, SportSectionCoachesMutation, ScheduleMutation):
    pass


schema = strawberry.Schema(query=Query, mutation=Mutation)
