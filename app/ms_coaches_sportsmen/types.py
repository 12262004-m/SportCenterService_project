import strawberry
from datetime import date
from app.ms_coaches_sportsmen.enums import GenderEnum


@strawberry.type
class CoachType:
    id: int
    last_name: str
    first_name: str
    middle_name: str
    gender: GenderEnum
    date_of_birth: date
    qualification: str
    experience: int


@strawberry.type
class SportsmanType:
    id: int
    last_name: str
    first_name: str
    middle_name: str
    gender: GenderEnum
    date_of_birth: date
    phone_number: str
    email: str
    registration_date: date
