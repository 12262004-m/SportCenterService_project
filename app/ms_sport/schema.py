from __future__ import annotations

import strawberry
from sqlalchemy.orm import Session
from strawberry.types import Info
from app.ms_sport.types import SportType
from app.ms_sport.enums import GraphQLSportTypeEnum
from app.ms_sport import crud
from app.ms_sport.models import Sport


@strawberry.type
class SportQuery:
    @strawberry.field
    def all_sports(self, info: Info) -> list[SportType]:
        db = info.context["db"]
        return crud.get_all_sports(db)

    @strawberry.field
    def sport_by_id(self, info: Info, sport_id: int) -> SportType:
        db = info.context["db"]
        sport = crud.get_sport_by_id(db, sport_id)
        if not sport:
            raise Exception("Спорт не найден")
        return SportType(id=sport.id, name=sport.name, type=sport.type)

@strawberry.type
class SportMutation:
    @strawberry.mutation
    def create_sport(self, info: Info, name: str, type: GraphQLSportTypeEnum) -> SportType:
        db: Session = info.context["db"]
        existing = db.query(Sport).filter_by(name=name).first()
        if existing:
            raise Exception(f"Спорт с названием '{name}' уже существует")

        new_sport = Sport(name=name, type=type.value)
        db.add(new_sport)
        db.commit()
        db.refresh(new_sport)
        return SportType(id=new_sport.id, name=new_sport.name, type=type)

    @strawberry.mutation
    def update_sport(self, info: Info, sport_id: int, name: str | None = None, type: GraphQLSportTypeEnum | None = None) -> SportType:
        db = info.context["db"]
        updated_sport = crud.update_sport(
            db, sport_id=sport_id,
            name=name,
            type=type.value if type else None
        )
        return SportType(id=updated_sport.id, name=updated_sport.name, type=updated_sport.type)

    @strawberry.mutation
    def delete_sport(self, info: Info, sport_id: int) -> bool:
        db = info.context["db"]
        return crud.delete_sport(db, sport_id)
