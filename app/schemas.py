# app/schemas.py
from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime


class ReportOut(BaseModel):
    id: int
    user_id: int
    type: str
    description: str
    photo_url: Optional[str] = None
    location: Optional[str] = None
    status: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True  # penting agar bisa baca dari SQLAlchemy model


class SearchResponse(BaseModel):
    total: int
    items: List[ReportOut]