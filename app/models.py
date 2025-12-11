# app/models.py
from sqlalchemy import Column, Integer, Text, String, Enum, TIMESTAMP
from sqlalchemy.sql import func
from app.database import Base
import enum


class ReportType(str, enum.Enum):
    lost = "lost"
    found = "found"


class ReportStatus(str, enum.Enum):
    open = "open"
    claimed = "claimed"
    closed = "closed"


class Report(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    type = Column(Enum(ReportType), nullable=False)
    description = Column(Text, nullable=False)
    photo_url = Column(String(255), nullable=True)
    location = Column(String(255), nullable=True)
    status = Column(Enum(ReportStatus), nullable=False, server_default="open")
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(
        TIMESTAMP,
        server_default=func.now(),
        onupdate=func.now(),
    )
