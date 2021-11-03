from fastapi import Response, Depends, APIRouter, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.orm import Session

from sql import crud
from sql.main import get_db

from utilities import http_security

router = APIRouter()
security = HTTPBasic()

sec = http_security.HTTPSecurity()


@router.get("/current/number/{association}", status_code=200)
def read_current(association, response: Response,
                 db: Session = Depends(get_db)):
    """
    Get current number of people at the given association as a number.

    Parameters:
        * association: a valid association.
    """
    print("Reading current")
    current = crud.get_current_people(db, association)
    return current


@router.get("/current/email/{association}", status_code=200)
def read_current_human(association, response: Response,
                       db: Session = Depends(get_db),
                       credentials: HTTPBasicCredentials = Depends(security)):
    """
    Get the emails of people at the given association.

    Parameters:
        * association: a valid association.
    """
    print("Checking security")
    if not sec.validate_admin(
            association,
            username=credentials.username,
            password=credentials.password):
        raise HTTPException(
            status_code=401,
            detail="Incorrect user or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    current = crud.get_current_people_data(db, association)
    print("Current emails", current)
    return current
