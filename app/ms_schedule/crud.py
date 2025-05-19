import datetime
from sqlalchemy.orm import Session
from app.ms_schedule.models import Schedule


def get_full_schedule(db: Session):
    return db.query(Schedule).all()


def create_schedule(db: Session, schedule_data: dict) -> Schedule:
    schedule = Schedule(**schedule_data)
    db.add(schedule)
    db.commit()
    db.refresh(schedule)
    return schedule


def get_schedule_for_section(db: Session, section_id: int) -> Schedule | None:
    return db.query(Schedule).filter(Schedule.section_id == section_id).first()


def get_schedule_for_sportHall(db: Session, hall_id: int) -> Schedule | None:
    return db.query(Schedule).filter(Schedule.hall_id == hall_id).first()


def update_schedule(db: Session, schedule_id: int, section_id: int | None = None,
                         hall_id: int | None = None, weekday: str | None = None,
                         start: datetime.time | None = None, end: datetime.time | None = None) -> Schedule:
    schedule = db.query(Schedule).filter(Schedule.id == schedule_id).first()
    if not schedule:
        raise Exception("Расписание не найдено")
    if section_id is not None:
        schedule.section_id = section_id
    if hall_id is not None:
        schedule.hall_id = hall_id
    if weekday is not None:
        schedule.weekday = weekday
    if start is not None:
        schedule.start = start
    if end is not None:
        schedule.end = end
    db.commit()
    db.refresh(schedule)
    return schedule


def delete_schedule(db: Session, schedule_id: int) -> bool:
    schedule = db.query(Schedule).filter(Schedule.id == schedule_id).first()
    if not schedule:
        raise Exception("Расписание не найдено")
    db.delete(schedule)
    db.commit()
    return True
