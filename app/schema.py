import strawberry
from .ms_coaches_sportsmen.schema import CoachSportsmenMutation, CoachSportsmenQuery
from .ms_auth.schema import UserMutation, UserQuery
from .ms_sport.schema import SportMutation, SportQuery

@strawberry.type
class Query(CoachSportsmenQuery, UserQuery, SportQuery):
    pass

@strawberry.type
class Mutation(CoachSportsmenMutation, UserMutation, SportMutation):
    pass


schema = strawberry.Schema(query=Query, mutation=Mutation)
print(schema)