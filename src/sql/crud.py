from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from . import models, schemas


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


def get_current_people(
        db: Session,
        association: str,
        _from: datetime = datetime.today().date(),
        _to: datetime = datetime.today().date() + timedelta(days=1)):
    accessed = db.query(models.Event).filter(
        models.Event.association == association).filter(
        models.Event.time > _from).filter(models.Event.time < _to).filter(
            models.Event.type == "access").count()
    exited = db.query(models.Event).filter(
        models.Event.association == association).filter(
        models.Event.time > _from).filter(models.Event.time < _to).filter(
            models.Event.type == "exit").count()
    if (exited - accessed) > 0:
        return 0
    return accessed - exited


def get_current_people_data(
        db: Session,
        association: str,
        _from: datetime = datetime.today().date(),
        _to: datetime = datetime.today().date() + timedelta(days=1)):
    accessed = db.query(models.Event).filter(
        models.Event.association == association).filter(
        models.Event.time > _from).filter(models.Event.time < _to).filter(
            models.Event.type == "access")
    exited = db.query(models.Event).filter(
        models.Event.association == association).filter(
        models.Event.time > _from).filter(models.Event.time < _to).filter(
            models.Event.type == "exit")
    results = {}
    for key, value in accessed.items():
        try:
            current = results[key]
        except Exception:
            current = 0
        current = current - 1
        results[key] = current
    for key, value in exited.items():
        try:
            current = results[key]
        except Exception:
            current = 0
        current = current + 1
        results[key] = current
    return ["%s\n" % key for key, value in results.items() if value == 1]


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
        models.Event.nif_nie == nif_nie
    ).filter(
        models.Event.email == email
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
