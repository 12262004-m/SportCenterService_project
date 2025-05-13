from sqlalchemy.orm import Session
from app.ms_sport.models import Sport, SportHall


def create_sport(db: Session, sport_data: dict) -> Sport:
    sport = Sport(**sport_data)
    db.add(sport)
    db.commit()
    db.refresh(sport)
    return sport


def get_all_sports(db: Session) -> list[Sport]:
    return db.query(Sport).all()


def get_sport_by_id(db: Session, sport_id: int) -> Sport | None:
    return db.query(Sport).filter(Sport.id == sport_id).first()


def update_sport(db: Session, sport_id: int, name: str | None = None, type: str | None = None) -> Sport:
    sport = db.query(Sport).filter(Sport.id == sport_id).first()
    if not sport:
        raise Exception("Спорт не найден")
    if name is not None:
        sport.name = name
    if type is not None:
        sport.type = type
    db.commit()
    db.refresh(sport)
    return sport


def delete_sport(db: Session, sport_id: int) -> bool:
    sport = db.query(Sport).filter(Sport.id == sport_id).first()
    if not sport:
        raise Exception("Спорт не найден")
    db.delete(sport)
    db.commit()
    return True


def create_sport_hall(db: Session, name: str, address: str, sport_ids: list[int]) -> SportHall:
    sports = db.query(Sport).filter(Sport.id.in_(sport_ids)).all()
    found_ids = {sport.id for sport in sports}
    missing_ids = set(sport_ids) - found_ids
    if missing_ids:
        raise Exception(f"Виды спорта с id {missing_ids} не найдены")
    sport_hall = SportHall(name=name, address=address, sports=sports)
    db.add(sport_hall)
    db.commit()
    db.refresh(sport_hall)
    return sport_hall


def get_all_sport_halls(db: Session) -> list[SportHall]:
    return db.query(SportHall).all()


def get_sport_hall_by_id(db: Session, hall_id: int) -> SportHall | None:
    return db.query(SportHall).filter(SportHall.id == hall_id).first()


def update_sport_hall(db: Session, hall_id: int, name: str | None = None, address: str | None = None, sport_ids: list[int] | None = None) -> SportHall:
    hall = db.query(SportHall).filter(SportHall.id == hall_id).first()
    if not hall:
        raise Exception("Зал не найден")
    if name is not None:
        hall.name = name
    if address is not None:
        hall.address = address
    if sport_ids is not None:
        sports = db.query(Sport).filter(Sport.id.in_(sport_ids)).all()
        found_ids = {sport.id for sport in sports}
        missing_ids = set(sport_ids) - found_ids
        if missing_ids:
            raise Exception(f"Виды спорта с id {missing_ids} не найдены")
        hall.sports = sports
    db.commit()
    db.refresh(hall)
    return hall


def delete_sport_hall(db: Session, hall_id: int) -> bool:
    hall = db.query(SportHall).filter(SportHall.id == hall_id).first()
    if not hall:
        raise Exception("Зал не найден")
    db.delete(hall)
    db.commit()
    return True
