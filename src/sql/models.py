"""
SQLAlchemy models
"""

from sqlalchemy import Column, Integer, String, DateTime
# from sqlalchemy.orm import relationship

from .database import Base


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, unique=True, index=True)
    type = Column(String, nullable=False)
    time = Column(DateTime, nullable=False)
    email = Column(String, nullable=False)
    nif_nie = Column(String, nullable=False)

    # items = relationship("Event")
