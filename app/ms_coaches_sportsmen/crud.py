from sqlalchemy.orm import Session
from app.ms_coaches_sportsmen import models
from app.ms_coaches_sportsmen.models import Coach, Sportsman


def get_coaches(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Coach).offset(skip).limit(limit).all()


def create_coach(db: Session, coach_data: dict) -> Coach:
    coach = Coach(**coach_data)
    db.add(coach)
    db.commit()
    db.refresh(coach)
    return coach


def get_sportsmen(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Sportsman).offset(skip).limit(limit).all()


def create_sportsmen(db: Session, sportsman_data: dict) -> Sportsman:
    sportsman = Sportsman(**sportsman_data)
    db.add(sportsman)
    db.commit()
    db.refresh(sportsman)
    return sportsman
