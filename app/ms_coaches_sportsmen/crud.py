from sqlalchemy.orm import Session
from app.ms_coaches_sportsmen.models import Coach, Sportsman
from datetime import date


def get_coaches(db: Session):
    return db.query(Coach).all()


def create_coach(db: Session, coach_data: dict) -> Coach:
    coach = Coach(**coach_data)
    db.add(coach)
    db.commit()
    db.refresh(coach)
    return coach


def get_sportsmen(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Sportsman).offset(skip).limit(limit).all()


def create_sportsmen(db: Session, sportsman_data: dict) -> Sportsman:
    sportsman = Sportsman(**sportsman_data)
    db.add(sportsman)
    db.commit()
    db.refresh(sportsman)
    return sportsman


def update_sportsmen(db: Session, sportsmen_id: int, first_name: str | None = None, last_name: str | None = None,
                     middle_name: str | None = None, date_of_birth: date | None = None, gender: str | None = None,
                     phone_number: str | None = None, email: str | None = None, registration_date: date | None = None) -> Sportsman:
    sportsman = db.query(Sportsman).filter(Sportsman.id == sportsmen_id).first()
    if not sportsman:
        raise Exception("Спортсмен не найден")
    if first_name is not None:
        sportsman.first_name = first_name
    if last_name is not None:
        sportsman.last_name = last_name
    if middle_name is not None:
        sportsman.middle_name = middle_name
    if date_of_birth is not None:
        sportsman.date_of_birth = date_of_birth
    if gender is not None:
        sportsman.gender = gender
    if phone_number is not None:
        sportsman.phone_number = phone_number
    if email is not None:
        sportsman.email = email
    if registration_date is not None:
        sportsman.registration_date = registration_date
    db.commit()
    db.refresh(sportsman)
    return sportsman
