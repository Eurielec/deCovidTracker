import os
import datetime

from fastapi import Response, Depends, APIRouter, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.orm import Session
from typing import List

from sql import crud, schemas
from sql.main import get_db

from utilities import validators, telegram_bot, http_security

router = APIRouter()
security = HTTPBasic()

validator = validators.Validator()
bot = telegram_bot.Bot()
sec = http_security.HTTPSecurity()

MAX_PEOPLE = int(os.environ.get("MAX_PEOPLE", 9))


@router.get("/")
def read_root():
    return {"Hello": "Eurielec"}


@router.post("/event", response_model=schemas.Event, status_code=202)
def create_event(event: schemas.EventCreate,
                 response: Response,
                 db: Session = Depends(get_db)):
    """
    Create an entry in the database with an access or exit value.

    * `type` (string): access | exit
    * `time` (datetime): datetime of the event
    * `email` (string): valid UPM email account
    * `nif_nie` (string): valid spanish ID
    """
    if not validator.validate_event(event):
        raise HTTPException(status_code=422, detail="Event data is not valid")

    result = crud.event_makes_sense(db, event.nif_nie, event.type)
    print(result)
    if not result:
        raise HTTPException(
            status_code=412, detail="Event is not natural")

    current = crud.get_current_people(db)
    if current >= MAX_PEOPLE and event.type == "access":
        bot.notify(
            message="Someone could not access Eurielec. 9 people already inside.",
            title='Warning',
        )
        raise HTTPException(
            status_code=409, detail="Already %s people inside" % MAX_PEOPLE)
    if event.type == "access":
        bot.notify(
            message="%s people @ Eurielec" % (current + 1),
            title="Warning" if (current + 1) >= 9 else "Info",
        )
    if event.type == "exit":
        bot.notify(
            message="%s people @ Eurielec" % ((current -
                                              1) if current > 0 else current),
            title='Info',
        )
    return crud.create_event(db=db, event=event)


@router.get("/events", response_model=List[schemas.Event])
def read_events(skip: int = 0, limit: int = 100,
                db: Session = Depends(get_db),
                credentials: HTTPBasicCredentials = Depends(security)):
    if not sec.validate_admin(
            username=credentials.username,
            password=credentials.password):
        raise HTTPException(
            status_code=401,
            detail="Incorrect user or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    events = crud.get_events(db, skip=skip, limit=limit)
    return events


@router.get("/events/{date}", response_model=List[schemas.Event])
def read_events_from_given_day(
    date, skip: int = 0, limit: int = 100,
        db: Session = Depends(get_db),
        credentials: HTTPBasicCredentials = Depends(security)):
    if not sec.validate_admin(
            username=credentials.username,
            password=credentials.password):
        raise HTTPException(
            status_code=401,
            detail="Incorrect user or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    try:
        if date == "today":
            events = crud.get_events_by_day(db)
            return events
        day = datetime.datetime.strptime(date, '%d-%m-%Y')
        to = day + datetime.timedelta(days=1)
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=400, detail="Provide date as: dd/mm/yyyy")
    events = crud.get_events_by_day(
        db, _from=day, _to=to, skip=skip, limit=limit)
    return events


@router.get("/events/{date1}/{date2}", response_model=List[schemas.Event])
def read_events_by_dates(
    date1, date2, skip: int = 0, limit: int = 100,
        db: Session = Depends(get_db),
        credentials: HTTPBasicCredentials = Depends(security)):
    if not sec.validate_admin(
            username=credentials.username,
            password=credentials.password):
        raise HTTPException(
            status_code=401,
            detail="Incorrect user or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    try:
        _from = datetime.datetime.strptime(date1, '%d-%m-%Y')
        _to = datetime.datetime.strptime(date2, '%d-%m-%Y')
    except Exception:
        raise HTTPException(
            status_code=400, detail="Provide date as: dd/mm/yyyy")
    events = crud.get_events_by_day(
        db, _from=_from, _to=_to, skip=skip, limit=limit)
    return events


@router.get("/event/{event_id}", response_model=schemas.Event)
def read_event(event_id: int, db: Session = Depends(get_db),
               credentials: HTTPBasicCredentials = Depends(security)):
    if not sec.validate_admin(
            username=credentials.username,
            password=credentials.password):
        raise HTTPException(
            status_code=401,
            detail="Incorrect user or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    db_event = crud.get_event(db, event_id=event_id)
    if db_event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return db_event
