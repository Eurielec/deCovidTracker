from datetime import datetime, timedelta

from fastapi import Response, Depends, APIRouter, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.orm import Session
from typing import List

from sql import crud, schemas
from sql.main import get_db

from utilities import validators, http_security, normalizer, helpers, jobs
from config import config

router = APIRouter()
security = HTTPBasic()

validator = validators.Validator()
normalizr = normalizer.Normalizer()
sec = http_security.HTTPSecurity()
j = jobs.Job()
c = config.Config()


@router.get("/event/{event_id}", response_model=schemas.Event)
def read_event(event_id: int, db: Session = Depends(get_db),
               credentials: HTTPBasicCredentials = Depends(security)):
    """
    Get a particular event and authenticate to access it depending on the
    owner association.

    Parameters:
        * event_id: event id number.
    """
    db_event = crud.get_event(db, event_id=event_id)
    if db_event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    association = crud.get_event(db, event_id=event_id).association
    if not sec.validate_admin(
            association,
            username=credentials.username,
            password=credentials.password):
        raise HTTPException(
            status_code=401,
            detail="Incorrect user or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return db_event


@router.get("/events/{association}/reset", status_code=200)
def trigger_close_open_events(
        association, db: Session = Depends(get_db),
        credentials: HTTPBasicCredentials = Depends(security)):
    if not sec.validate_admin(
            association,
            username=credentials.username,
            password=credentials.password):
        raise HTTPException(
            status_code=401,
            detail="Incorrect user or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    j.close_association_events(db, association)
    return {"result": "success"}


@router.post("/event", response_model=schemas.Event, status_code=202)
def create_event(event: schemas.EventCreate,
                 response: Response,
                 db: Session = Depends(get_db)):
    """
    Create an entry in the database with an access or exit value.

    Body:
        * `type` (string): access | exit
        * `time` (datetime): datetime of the event
        * `email` (string): valid UPM email account
        * `nif_nie` (string): valid spanish ID
        * `association` (string): association name
    """
    if not validator.validate_event(event):
        raise HTTPException(status_code=422, detail="Event data is not valid")
    event = normalizr.normalize_event(event)
    association_config = c.get_association_config(event.association)
    max_people = association_config["max_people"]
    result = crud.event_makes_sense(
        db, event.nif_nie, event.email, event.type, event.association)
    if not result:
        raise HTTPException(
            status_code=412, detail="Event is not natural")
    current = crud.get_current_people(db, event.association)
    helpers.evaluate_and_notify(
        current, event.association, max_people, event.type)
    if current >= max_people and event.type == "access":
        raise HTTPException(
            status_code=409, detail="Already %s people inside" % max_people)
    return crud.create_event(db=db, event=event)


@router.get("/events/{association}", response_model=List[schemas.Event])
def read_events(association, skip: int = 0, limit: int = 300,
                db: Session = Depends(get_db),
                credentials: HTTPBasicCredentials = Depends(security)):
    """
    Get all the events of the given association. By default limited to the last
    300.

    Parameters:
        * association: a valid association.
    """
    if not sec.validate_admin(
            association,
            username=credentials.username,
            password=credentials.password):
        raise HTTPException(
            status_code=401,
            detail="Incorrect user or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    events = crud.get_events(db, association, skip=skip, limit=limit)
    return events


@router.get("/events/{association}/{date}", response_model=List[schemas.Event])
def read_events_from_given_day(
    association, date, skip: int = 0, limit: int = 100,
        db: Session = Depends(get_db),
        credentials: HTTPBasicCredentials = Depends(security)):
    """
    Get events for a given association for a given date. Date can be `today`
    for ease of use.

    Parameters:
        * association: a valid association.
        * date: dd-mm-yyyy.
    """
    if not sec.validate_admin(
            association,
            username=credentials.username,
            password=credentials.password):
        raise HTTPException(
            status_code=401,
            detail="Incorrect user or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    try:
        if date == "today":
            events = crud.get_events_by_day(
                db, association, _from=datetime.today(
                ).date(), _to=(datetime.today().date() + timedelta(days=1)))
            return events
        day = datetime.strptime(date, '%d-%m-%Y')
        to = day + timedelta(days=1)
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=400, detail="Provide date as: dd/mm/yyyy")
    events = crud.get_events_by_day(
        db, association, _from=day, _to=to, skip=skip, limit=limit)
    return events


@router.get("/events/{association}/{date1}/{date2}",
            response_model=List[schemas.Event])
def read_events_by_dates(
    association, date1, date2, skip: int = 0, limit: int = 100,
        db: Session = Depends(get_db),
        credentials: HTTPBasicCredentials = Depends(security)):
    """
    Get events for a given association between two given dates.

    Parameters:
        * association: a valid association.
        * date1: dd-mm-yyyy.
        * date2: dd-mm-yyyy.
        > Note dates are inclusive.
    """
    if not sec.validate_admin(
            association,
            username=credentials.username,
            password=credentials.password):
        raise HTTPException(
            status_code=401,
            detail="Incorrect user or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    try:
        _from = datetime.strptime(date1, '%d-%m-%Y')
        _to = datetime.strptime(date2, '%d-%m-%Y') + timedelta(days=1)
    except Exception:
        raise HTTPException(
            status_code=400, detail="Provide dates as: dd-mm-yyyy")
    events = crud.get_events_by_day(
        db, association, _from=_from, _to=_to, skip=skip, limit=limit)
    return events
