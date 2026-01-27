from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class ListenEvent(Base):
    __tablename__ = "listen_events"

    id = Column(Integer, primary_key=True, index=True)
    artist = Column(String, index=True)
    song = Column(String)
    duration = Column(Float)
    userId = Column(String, index=True)
    state = Column(String, index=True)
    level = Column(String, index=True)
    genre = Column(String, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)


class AuthEvent(Base):
    __tablename__ = "auth_events"

    id = Column(Integer, primary_key=True, index=True)
    success = Column(Boolean)
    userId = Column(String, index=True)
    state = Column(String, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)


class StatusChangeEvent(Base):
    __tablename__ = "status_change_events"

    id = Column(Integer, primary_key=True, index=True)
    level = Column(String, index=True)
    userId = Column(String, index=True)
    state = Column(String, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
