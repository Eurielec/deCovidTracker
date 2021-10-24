from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session


from sql.main import get_db


from config import config
from utilities import jobs

router = APIRouter()

c = config.Config()
j = jobs.Job()


@router.get("/jobs/mail", status_code=200)
def trigger_mail(db: Session = Depends(get_db)):
    j.mail(db)
    return {"result": "success"}


@router.get("/jobs/close", status_code=200)
def trigger_close_open_events(db: Session = Depends(get_db)):
    j.close_open_events(db)
    return {"result": "success"}
