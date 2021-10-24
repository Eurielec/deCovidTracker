"""
Pydantic models

> We use Pydantic because it provides speed optimizations with Fastapi
"""

from pydantic import BaseModel
import datetime


# Common attributes while creating or reading
class EventBase(BaseModel):
    type: str
    email: str
    nif_nie: str
    time: datetime.datetime
    association: str


# Any additional attributes needed for creation
class EventCreate(EventBase):
    """
    Same event with aditional values needed for creation.
    """


# Reading/returning attributes we know when reading
class Event(EventBase):
    """
    An event object to register access or exit events.
    """
    id: int

    class Config:
        # Not declaring a type, but setting a config option
        # Allows to access id = data["id"] and as attribute id = data.id
        # SQLAlchemy lazy loads, and won't load untill attribute is called
        orm_mode = True
