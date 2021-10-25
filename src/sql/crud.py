from sqlalchemy.orm import Session
from sqlalchemy import _or
from datetime import datetime, timedelta

from . import models, schemas
from utilities import helpers


def get_event(db: Session, event_id: int):
    return db.query(models.Event).filter(models.Event.id == event_id).first()


def get_events(db: Session, association: str, skip: int = 0, limit: int = 300):
    return db.query(models.Event).filter(
        models.Event.association == association
    ).offset(skip).limit(limit).all()


def get_events_by_email(db: Session, email: str):
    return db.query(
        models.Event).filter(models.Event.email == email).all()


def get_events_by_day(
        db: Session,
        association: str,
        skip: int = 0, limit: int = 300,
        _from: datetime = datetime.today().date(),
        _to: datetime = datetime.today().date() + timedelta(days=1)):
    return db.query(models.Event).filter(
        models.Event.association == association).filter(
        models.Event.time > _from).filter(models.Event.time < _to).all()


def get_accessed(
        db: Session,
        association: str,
        skip: int = 0, limit: int = 0,
        _from: datetime = datetime.today().date(),
        _to: datetime = datetime.today().date() + timedelta(days=1)):
    accessed = db.query(models.Event).filter(
        models.Event.association == association).filter(
        models.Event.time > _from).filter(models.Event.time < _to).filter(
            models.Event.type == "access")
    return accessed


def get_exited(
        db: Session,
        association: str,
        skip: int = 0, limit: int = 0,
        _from: datetime = datetime.today().date(),
        _to: datetime = datetime.today().date() + timedelta(days=1)):
    exited = db.query(models.Event).filter(
        models.Event.association == association).filter(
        models.Event.time > _from).filter(models.Event.time < _to).filter(
            models.Event.type == "exit")
    return exited


def get_current_people(
        db: Session,
        association: str,
        _from: datetime = datetime.today().date(),
        _to: datetime = datetime.today().date() + timedelta(days=1)):
    accessed = get_accessed(db, association, _from=_from, _to=_to).count()
    exited = get_exited(db, association, _from=_from, _to=_to).count()
    if (accessed - exited) < 0:
        return 0
    return accessed - exited


def get_current_people_data(
        db: Session,
        association: str,
        _from: datetime = datetime.today().date(),
        _to: datetime = datetime.today().date() + timedelta(days=1)):
    accessed = get_accessed(db, association, _from=_from, _to=_to)
    exited = get_exited(db, association, _from=_from, _to=_to)
    inside = helpers.calculate_people_inside(accessed, exited)
    return inside


def get_events_by_nif_nie(db: Session, nif_nie: str):
    return db.query(
        models.Event).filter(models.Event.nif_nie == nif_nie).all()


def event_makes_sense(db: Session, nif_nie: str, email: str,
                      type: str, association: str):
    last_event = db.query(
        models.Event
    ).filter(
        models.Event.association == association
    ).filter(
        _or(models.Event.nif_nie == nif_nie, models.Event.email == email)
    ).order_by(-models.Event.id).first()
    print(last_event, type, nif_nie, association)
    if last_event is None:
        return True
    if last_event.type != type:
        return True
    return False


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
