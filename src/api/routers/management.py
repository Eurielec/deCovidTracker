from fastapi import Depends, APIRouter, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.orm import Session

from sql import crud, schemas
from sql.main import get_db

from utilities import http_security
from config import config

router = APIRouter()
security = HTTPBasic()

sec = http_security.HTTPSecurity()
c = config.Config()


@router.delete("/event/{event_id}", response_model=schemas.Event)
def delete_event(event_id: int, db: Session = Depends(get_db),
                 credentials: HTTPBasicCredentials = Depends(security)):
    """
    Delete a particular event and authenticate to access it depending on the
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
    try:
        crud.delete_event(db, event_id=event_id)
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Couldn't delete event",
        )
    return db_event
