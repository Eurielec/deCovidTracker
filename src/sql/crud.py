from sqlalchemy.orm import Session
from sqlalchemy import or_
from datetime import datetime, timedelta, date

from . import models, schemas
from utilities import helpers


def create_event(db: Session, event: schemas.EventCreate):
    try:
        db_event = models.Event(
            type=event.type,
            time=datetime.now(),
            email=event.email,
            nif_nie=event.nif_nie,
            association=event.association)
    except Exception:
        db_event = models.Event(
            type=event["type"],
            time=datetime.now(),
            email=event["email"],
            nif_nie=event["nif_nie"],
            association=event["association"])
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event


def get_event(db: Session, event_id: int):
    return db.query(models.Event).filter(models.Event.id == event_id).first()


def delete_event(db: Session, event_id: int):
    db.query(models.Event).filter(models.Event.id == event_id).delete()
    db.commit()
    return True


def get_events(db: Session, association: str, skip: int = 0, limit: int = 300):
    return db.query(models.Event).filter(
        models.Event.association == association
    ).offset(skip).limit(limit).all()


def get_events_by_email(db: Session, email: str):
    return db.query(
        models.Event).filter(models.Event.email == email).all()


def get_events_by_nif_nie(db: Session, nif_nie: str):
    return db.query(
        models.Event).filter(models.Event.nif_nie == nif_nie).all()


def get_email_by_nif_nie(db: Session, nif_nie: str):
    return db.query(models.Event).filter(
        models.Event.nif_nie == nif_nie).last().email


def get_events_by_day(
        db: Session,
        association: str,
        skip: int = 0, limit: int = 300,
        _from: datetime = datetime.combine(date.today(), datetime.min.time()),
        _to: datetime = (datetime.combine(date.today(), datetime.min.time()) +
                         timedelta(days=1))):
    return db.query(models.Event).filter(
        models.Event.association == association).filter(
        models.Event.time > _from).filter(
        models.Event.time < _to).offset(skip).limit(limit).all()


def get_accessed(
        db: Session,
        association: str,
        _from: datetime = datetime.combine(date.today(), datetime.min.time()),
        _to: datetime = (datetime.combine(date.today(), datetime.min.time()) +
                         timedelta(days=1))):
    accessed = db.query(models.Event).filter(
        models.Event.association == association).filter(
        models.Event.time > _from).filter(models.Event.time < _to).filter(
            models.Event.type == "access")
    return accessed


def get_exited(
        db: Session,
        association: str,
        _from: datetime = datetime.combine(date.today(), datetime.min.time()),
        _to: datetime = (datetime.combine(date.today(), datetime.min.time())
                         + timedelta(days=1))):
    exited = db.query(models.Event).filter(
        models.Event.association == association).filter(
        models.Event.time > _from).filter(models.Event.time < _to).filter(
            models.Event.type == "exit")
    return exited


def get_current_people(
        db: Session,
        association: str,
        _from: datetime = datetime.combine(date.today(), datetime.min.time()),
        _to: datetime = (datetime.combine(date.today(), datetime.min.time())
                         + timedelta(days=1))):
    accessed = get_accessed(db, association, _from=_from, _to=_to).count()
    exited = get_exited(db, association, _from=_from, _to=_to).count()
    print(accessed-exited)
    if (accessed - exited) < 0:
        return 0
    return accessed - exited


def get_current_people_data(
        db: Session,
        association: str,
        _from: datetime = datetime.combine(date.today(), datetime.min.time()),
        _to: datetime = (datetime.combine(date.today(), datetime.min.time()) +
                         timedelta(days=1))):
    accessed = get_accessed(db, association, _from=_from, _to=_to)
    exited = get_exited(db, association, _from=_from, _to=_to)
    inside = helpers.calculate_people_inside(accessed, exited)
    print(inside)
    return inside


def event_makes_sense(db: Session, nif_nie: str, email: str,
                      type: str, association: str):
    last_event = db.query(
        models.Event
    ).filter(
        models.Event.association == association
    ).filter(
        or_(models.Event.nif_nie == nif_nie, models.Event.email == email)
    ).order_by(-models.Event.id).first()
    if last_event is None and type == "exit":
        return False
    if last_event is None and type == "access":
        return True
    if last_event.type != type:
        return True
    return False
