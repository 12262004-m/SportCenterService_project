import strawberry
from app.ms_sport.enums import GraphQLSportTypeEnum

@strawberry.type
class SportType:
    id: int
    name: str
    type: GraphQLSportTypeEnum

