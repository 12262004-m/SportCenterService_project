from __future__ import annotations

from sqlalchemy.orm import Session
from app.ms_sport.models import Sport

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
