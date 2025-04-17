import strawberry
from datetime import date
from sqlalchemy.orm import Session
from app.database import get_db
from app.ms_coaches_sportsmen import crud
from app.ms_coaches_sportsmen.enums import GenderEnum
from app.ms_coaches_sportsmen.types import CoachType, SportsmanType


@strawberry.type
class CoachSportsmenMutation:
    @strawberry.mutation
    def create_coach(
            self,
            last_name: str,
            first_name: str,
            middle_name: str,
            gender: GenderEnum,
            date_of_birth: date,
            qualification: str,
            experience: int,
    ) -> CoachType:
        db: Session = next(get_db())

        coach_data = {
            "last_name": last_name,
            "first_name": first_name,
            "middle_name": middle_name,
            "gender": gender.value,
            "date_of_birth": date_of_birth,
            "qualification": qualification,
            "experience": experience,
        }

        coach = crud.create_coach(db, coach_data)

        return CoachType(
            id=coach.id,
            last_name=coach.last_name,
            first_name=coach.first_name,
            middle_name=coach.middle_name,
            gender=coach.gender,
            date_of_birth=coach.date_of_birth,
            qualification=coach.qualification,
            experience=coach.experience,
        )

    @strawberry.mutation
    def create_sportsman(
            self,
            last_name: str,
            first_name: str,
            middle_name: str,
            gender: GenderEnum,
            date_of_birth: date,
            phone_number: str,
            email: str,
            registration_date: date
    ) -> SportsmanType:
        db: Session = next(get_db())
        sportsman = {
            "last_name": last_name,
            "first_name": first_name,
            "middle_name": middle_name,
            "gender": gender.value,
            "date_of_birth": date_of_birth,
            "phone_number": phone_number,
            "email": email,
            "registration_date": registration_date,
        }
        sportsman = crud.create_sportsmen(db, sportsman)
        return SportsmanType(
            id=sportsman.id,
            last_name=sportsman.last_name,
            first_name=sportsman.first_name,
            middle_name=sportsman.middle_name,
            gender=sportsman.gender,
            date_of_birth=sportsman.date_of_birth,
            phone_number=sportsman.phone_number,
            email=sportsman.email,
            registration_date=sportsman.registration_date,
        )


@strawberry.type
class CoachSportsmenQuery:
    @strawberry.field
    def get_all_coaches(self) -> list[CoachType]:
        db: Session = next(get_db())
        return [CoachType(
            id=coach.id,
            last_name=coach.last_name,
            first_name=coach.first_name,
            middle_name=coach.middle_name,
            gender=coach.gender,
            date_of_birth=coach.date_of_birth,
            qualification=coach.qualification,
            experience=coach.experience
        ) for coach in crud.get_coaches(db)]

    @strawberry.field
    def get_all_athletes(self) -> list[SportsmanType]:
        db: Session = next(get_db())
        return [SportsmanType(
            id=sportsman.id,
            last_name=sportsman.last_name,
            first_name=sportsman.first_name,
            middle_name=sportsman.middle_name,
            gender=sportsman.gender,
            date_of_birth=sportsman.date_of_birth,
            phone_number=sportsman.phone_number,
            email=sportsman.email,
            registration_date=sportsman.registration_date,
        ) for sportsman in crud.get_sportsmen(db)]
