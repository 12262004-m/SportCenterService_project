import strawberry
from strawberry.types import Info
from typing import List
from datetime import date

from app.ms_coaches_sportsmen.models import Coach
from app.ms_coaches_sportsmen.types import SportsmanType
from app.ms_sections.models import SportSection
from app.ms_sections.types import SportSectionType, SportSectionCoachType
from app.ms_sections import crud
from app.ms_sport.types import SportType


@strawberry.type
class SportSectionQuery:
    @strawberry.field()
    def get_all_sport_sections(self, info: Info) -> List[SportSectionType]:
        db = info.context["db"]
        return crud.get_all_sport_sections(db)

    @strawberry.field()
    def find_sport_section_by_id(self, info: Info, section_id: int) -> SportSectionType:
        db = info.context["db"]
        section = crud.get_sport_section_by_id(db, section_id)
        if not section:
            raise Exception("Секция не найдена")
        return SportSectionType(
            id=section.id,
            title=section.title,
            sport=SportType(id=section.sport.id, name=section.sport.name, type=section.sport.type),
            description=section.description,
            capacity=section.capacity,
            sportsmen=[SportsmanType(id=s.id, last_name=s.last_name, first_name=s.first_name,
                                                         middle_name=s.middle_name, gender=s.gender, date_of_birth=s.date_of_birth,
                                                         phone_number=s.phone_number, email=s.email,
                                                         registration_date=s.registration_date) for s in section.sportsmen])


@strawberry.type
class SportSectionMutation:
    @strawberry.mutation()
    def create_sport_section(self, info: Info, title: str, description: str, capacity: int,
                             sport_id: int, sportsmen_ids: list[int]) -> SportSectionType:
        db = info.context["db"]
        section = crud.create_sport_section(db, title=title, description=description, capacity=capacity,
                                            sport_id=sport_id, sportsmen_ids=sportsmen_ids)
        return SportSectionType(id=section.id, title=section.title,
                                description=section.description, capacity=section.capacity,
                                sport=SportType(id=section.sport.id, name=section.sport.name, type=section.sport.type),
                                sportsmen=[SportsmanType(id=s.id, last_name=s.last_name, first_name=s.first_name,
                                                         middle_name=s.middle_name, gender=s.gender, date_of_birth=s.date_of_birth,
                                                         phone_number=s.phone_number, email=s.email,
                                                         registration_date=s.registration_date) for s in section.sportsmen])

    @strawberry.mutation()
    def update_sport_section(self, info: Info, section_id: int, title: str | None = None,
                             description: str | None = None, capacity: int | None = None,
                             sport_id: int | None = None, sportsmen_ids: list[int] | None = None) -> SportSectionType:
        db = info.context["db"]
        section = crud.update_sport_section(db, section_id, title, description, capacity, sport_id, sportsmen_ids)
        return SportSectionType(id=section.id, title=section.title, description=section.description, capacity=section.capacity,
                                sport=SportType(id=section.sport.id, name=section.sport.name, type=section.sport.type),
                                sportsmen=[SportsmanType(id=s.id, last_name=s.last_name, first_name=s.first_name,
                                                         middle_name=s.middle_name, gender=s.gender, date_of_birth=s.date_of_birth,
                                                         phone_number=s.phone_number, email=s.email,
                                                         registration_date=s.registration_date) for s in section.sportsmen])

    @strawberry.mutation()
    def delete_sport_section(self, info: Info, section_id: int) -> bool:
        db = info.context["db"]
        return crud.delete_sport_section(db, section_id)


@strawberry.type
class SportSectionCoachesQuery:
    @strawberry.field()
    def get_all_sport_sections(self, info: Info) -> List[SportSectionType]:
        db = info.context["db"]
        return crud.get_all_sport_sections(db)

    @strawberry.field()
    def find_sport_section_by_id(self, info: Info, section_id: int) -> SportSectionType:
        db = info.context["db"]
        section = crud.get_sport_section_by_id(db, section_id)
        if not section:
            raise Exception("Секция не найдена")
        return SportSectionType(
            id=section.id,
            title=section.title,
            sport=SportType(id=section.sport.id, name=section.sport.name, type=section.sport.type),
            description=section.description,
            capacity=section.capacity,
            sportsmen=[SportsmanType(id=s.id, last_name=s.last_name, first_name=s.first_name,
                                                         middle_name=s.middle_name, gender=s.gender, date_of_birth=s.date_of_birth,
                                                         phone_number=s.phone_number, email=s.email,
                                                         registration_date=s.registration_date) for s in section.sportsmen])

    @strawberry.field()
    def add_new_sportsman_to_section(self, info: Info, section_id: int, sportsman_id: int) -> SportSectionType:
        db = info.context["db"]
        section = crud.add_sportsman_to_section(db, section_id, sportsman_id)
        return SportSectionType(
            id=section.id,
            title=section.title,
            sport=SportType(id=section.sport.id, name=section.sport.name, type=section.sport.type),
            description=section.description,
            capacity=section.capacity,
            sportsmen=[SportsmanType(id=s.id, last_name=s.last_name, first_name=s.first_name,
                                                         middle_name=s.middle_name, gender=s.gender, date_of_birth=s.date_of_birth,
                                                         phone_number=s.phone_number, email=s.email,
                                                         registration_date=s.registration_date) for s in section.sportsmen])

    @strawberry.field()
    def delete_sportsman_from_section(self, info: Info, section_id: int, sportsman_id: int) -> str:
        db = info.context["db"]
        section = crud.remove_sportsman_from_section(db, section_id, sportsman_id)
        if section:
            return "Спортсмен успешно удален из секции"
        return "Ошибка при удалении спортсмена"


@strawberry.type
class SportSectionCoachesMutation:
    @strawberry.mutation()
    def create_sport_section_coach(self, info: Info, coach_id: int, section_id: int,
                                   start: date, end: date) -> SportSectionCoachType:
        db = info.context["db"]
        section_coach_data = {
            "coach_id": coach_id,
            "section_id": section_id,
            "start": start,
            "end": end,
        }
        section_coach = crud.create_sport_section_coach(db, section_coach_data)
        coach = db.query(Coach).filter(Coach.id == section_coach.coach_id).first()
        section = db.query(SportSection).filter(SportSection.id == section_coach.section_id).first()
        return SportSectionCoachType(id=section_coach.id, coach=coach,
                                     section=section, start=section_coach.start,
                                     end=section_coach.end)

    @strawberry.mutation()
    def delete_sport_section_coach(self, info: Info, section_coach_id: int) -> bool:
        db = info.context["db"]
        return crud.delete_sport_section_coach(db, section_coach_id)
