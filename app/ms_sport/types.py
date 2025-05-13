import strawberry
from app.ms_sport.enums import GraphQLSportTypeEnum


@strawberry.type
class SportType:
    id: int
    name: str
    type: GraphQLSportTypeEnum


@strawberry.type
class SportHallType:
    id: int
    name: str
    address: str
    sports: list[SportType]
