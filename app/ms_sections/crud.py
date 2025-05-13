from sqlalchemy.orm import Session
from app.ms_sections.models import SportSection, SportSectionCoach
from app.ms_coaches_sportsmen.models import Sportsman


def create_sport_section(db: Session, title: str, sport_id: int, description: str,
                         capacity: int, sportsmen_ids: list[int]) -> SportSection:
    sportsmen = db.query(Sportsman).filter(Sportsman.id.in_(sportsmen_ids)).all()
    found_ids = {sportsman.id for sportsman in sportsmen}
    missing_ids = set(sportsmen_ids) - found_ids
    if missing_ids:
        raise Exception(f"Спортсмены с id {missing_ids} не найдены")
    sport_section = SportSection(title=title,
                                 sport_id=sport_id,
                                 description=description,
                                 capacity=capacity,
                                 sportsmen=sportsmen)
    db.add(sport_section)
    db.commit()
    db.refresh(sport_section)
    return sport_section


def get_all_sport_sections(db: Session) -> list[SportSection]:
    return db.query(SportSection).all()


def get_sport_section_by_id(db: Session, section_id: int) -> SportSection | None:
    return db.query(SportSection).filter(SportSection.id == section_id).first()


def update_sport_section(db: Session, section_id: int, title: str | None = None,
                         description: str | None = None, capacity: int | None = None,
                         sport_id: int | None = None, sportsmen_ids: list[int] | None = None) -> SportSection:
    section = db.query(SportSection).filter(SportSection.id == section_id).first()
    if not section:
        raise Exception("Спортивная секция не найдена")
    if title is not None:
        section.title = title
    if description is not None:
        section.description = description
    if capacity is not None:
        section.capacity = capacity
    if sport_id is not None:
        section.sport_id = sport_id
    if sportsmen_ids is not None:
        sportsmen = db.query(Sportsman).filter(Sportsman.id.in_(sportsmen_ids)).all()
        found_ids = {sport.id for sport in sportsmen}
        missing_ids = set(sportsmen_ids) - found_ids
        if missing_ids:
            raise Exception(f"Спортсмены с id {missing_ids} не найдены")
    db.commit()
    db.refresh(section)
    return section


def delete_sport_section(db: Session, section_id: int) -> bool:
    section = db.query(SportSection).filter(SportSection.id == section_id).first()
    if not section:
        raise Exception("Спортивная секция не найдена")
    db.delete(section)
    db.commit()
    return True


def create_sport_section_coach(db: Session, section_coach_data: dict) -> SportSectionCoach:
    section_coach = SportSectionCoach(**section_coach_data)
    db.add(section_coach)
    db.commit()
    db.refresh(section_coach)
    return section_coach


def delete_sport_section_coach(db: Session, section_coach_id: int) -> bool:
    coach_section = db.query(SportSectionCoach).filter(SportSectionCoach.id == section_coach_id).first()
    if not coach_section:
        raise Exception("Тренер не найден в секции")
    db.delete(coach_section)
    db.commit()
    return True


def add_sportsman_to_section(db: Session, section_id: int, sportsman_id: int) -> SportSection:
    section = db.query(SportSection).filter(SportSection.id == section_id).first()
    sportsman = db.query(Sportsman).filter(Sportsman.id == sportsman_id).first()
    if not section or not sportsman:
        raise Exception("Секция или спортсмен не найдены")
    section.sportsmen.append(sportsman)
    db.commit()
    db.refresh(section)
    return section


def remove_sportsman_from_section(db: Session, section_id: int, sportsman_id: int) -> bool:
    section = db.query(SportSection).filter(SportSection.id == section_id).first()
    sportsman = db.query(Sportsman).filter(Sportsman.id == sportsman_id).first()

    if not section or not sportsman:
        raise Exception("Секция или спортсмен не найдены")

    section.sportsmen.remove(sportsman)
    db.commit()
    db.refresh(section)
    return True