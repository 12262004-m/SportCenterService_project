import strawberry
from app.ms_sport.models import SportTypeEnum

GraphQLSportTypeEnum = strawberry.enum(SportTypeEnum, name="SportTypeEnum")
