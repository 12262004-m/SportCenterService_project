import strawberry
from .ms_coaches_sportsmen.schema import CoachSportsmenMutation, CoachSportsmenQuery
from .ms_auth.schema import UserMutation, UserQuery

@strawberry.type
class Query(CoachSportsmenQuery, UserQuery):
    pass

@strawberry.type
class Mutation(CoachSportsmenMutation, UserMutation):
    pass


schema = strawberry.Schema(query=Query, mutation=Mutation)
print(schema)