# app/main.py
from fastapi import FastAPI, Depends, Query
from typing import Optional

from sqlalchemy.orm import Session

from app.database import get_db
from app import crud, schemas

app = FastAPI(
    title="Lost & Found Search Service",
    version="1.0.0",
)


@app.get("/api/search", response_model=schemas.SearchResponse)
def search_reports(
    keyword: str = Query(..., min_length=3),
    location: Optional[str] = None,
    type: Optional[str] = Query(None, pattern="^(lost|found)$"),
    status: Optional[str] = Query(None, pattern="^(open|claimed|closed)$"),
    db: Session = Depends(get_db),
):
    """
    Endpoint yang akan dipanggil dari Laravel:
    GET /api/search?keyword=...&location=...&type=...&status=...
    """
    reports = crud.search_reports(
        db=db,
        keyword=keyword,
        location=location,
        type_=type,
        status=status,
    )
    return schemas.SearchResponse(
        total=len(reports),
        items=reports,  # FastAPI + orm_mode akan konversi ke ReportOut
    )


@app.get("/api/search/matches/{report_id}", response_model=schemas.SearchResponse)
def search_matches(
    report_id: int,
    db: Session = Depends(get_db),
):
    """
    Endpoint untuk menemukan laporan lain yang mirip dengan report tertentu.
    Misalnya untuk rekomendasi 'potensi kecocokan'.
    """
    reports = crud.find_matches_for_report(db, report_id=report_id)
    return schemas.SearchResponse(
        total=len(reports),
        items=reports,
    )


@app.get("/")
def root():
    return {"message": "Search service up. Use /api/search or /api/search/matches/{id}."}
