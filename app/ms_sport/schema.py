import strawberry
from strawberry.types import Info
from app.ms_sport.types import SportType, SportHallType
from app.ms_sport.enums import GraphQLSportTypeEnum
from app.ms_sport import crud
from app.ms_sport.models import Sport, SportHall


@strawberry.type
class SportQuery:
    @strawberry.field()
    def get_all_sports(self, info: Info) -> list[SportType]:
        db = info.context["db"]
        return crud.get_all_sports(db)

    @strawberry.field()
    def find_sport_by_id(self, info: Info, sport_id: int) -> SportType:
        db = info.context["db"]
        sport = crud.get_sport_by_id(db, sport_id)
        if not sport:
            raise Exception("Спорт не найден")
        return SportType(id=sport.id, name=sport.name, type=sport.type)


@strawberry.type
class SportMutation:
    @strawberry.mutation()
    def create_sport(self, info: Info, name: str, type: GraphQLSportTypeEnum) -> SportType:
        db = info.context["db"]
        if db.query(Sport).filter_by(name=name).first():
            raise Exception(f"Спорт с названием '{name}' уже существует")
        sport_data = {
            "name": name,
            "type": type.value
        }
        sport = crud.create_sport(db, sport_data)
        return SportType(id=sport.id, name=sport.name, type=type)

    @strawberry.mutation()
    def update_sport(self, info: Info, sport_id: int, name: str | None = None, type: GraphQLSportTypeEnum | None = None) -> SportType:
        db = info.context["db"]
        updated_sport = crud.update_sport(db, sport_id=sport_id, name=name, type=type.value if type else None)
        return SportType(id=updated_sport.id, name=updated_sport.name, type=updated_sport.type)

    @strawberry.mutation()
    def delete_sport(self, info: Info, sport_id: int) -> bool:
        db = info.context["db"]
        return crud.delete_sport(db, sport_id)


@strawberry.type
class SportHallQuery:
    @strawberry.field()
    def get_all_sport_halls(self, info: Info) -> list[SportHallType]:
        db = info.context["db"]
        return crud.get_all_sport_halls(db)

    @strawberry.field()
    def find_sport_hall_by_id(self, info: Info, hall_id: int) -> SportHallType:
        db = info.context["db"]
        hall = crud.get_sport_hall_by_id(db, hall_id)
        if not hall:
            raise Exception("Зал не найден")
        return SportHallType(id=hall.id,
                             name=hall.name,
                             address=hall.address,
                             sports=[SportType(id=s.id, name=s.name, type=s.type) for s in hall.sports]
                             )


@strawberry.type
class SportHallMutation:
    @strawberry.mutation()
    def create_sport_hall(self, info: Info, name: str, address: str, sport_ids: list[int]) -> SportHallType:
        db = info.context["db"]
        if db.query(SportHall).filter_by(name=name).first():
            raise Exception(f"Спортзал '{address}' уже существует")
        hall = crud.create_sport_hall(db, name=name, address=address, sport_ids=sport_ids)
        return SportHallType(id=hall.id,
                             name=hall.name,
                             address=hall.address,
                             sports=[SportType(id=s.id, name=s.name, type=s.type) for s in hall.sports]
                             )

    @strawberry.mutation()
    def update_sport_hall(self, info: Info, hall_id: int, name: str | None = None, address: str | None = None,
                          sport_ids: list[int] | None = None) -> SportHallType:
        db = info.context["db"]
        hall = crud.update_sport_hall(db, hall_id, name, address, sport_ids)
        return SportHallType(id=hall.id,
                             name=hall.name,
                             address=hall.address,
                             sports=[SportType(id=s.id, name=s.name, type=s.type) for s in hall.sports]
                             )

    @strawberry.mutation()
    def delete_sport_hall(self, info: Info, hall_id: int) -> bool:
        db = info.context["db"]
        return crud.delete_sport_hall(db, hall_id)
