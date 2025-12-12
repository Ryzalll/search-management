from fastapi import FastAPI, Depends, Query, HTTPException
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
    location: str | None = None,
    type: str | None = Query(None, pattern="^(lost|found)$"),
    status: str | None = Query(None, pattern="^(open|claimed|closed)$"),
    db: Session = Depends(get_db),
):
    try:
        reports = crud.search_reports(
            db=db,
            keyword=keyword,
            location=location,
            type_=type,
            status=status,
        )
    except Exception as e:
        # kalau ada error DB betulan
        raise HTTPException(status_code=500, detail=f"Database error: {e}")

    # Kalau tidak ada hasil → ini BUKAN error
    return schemas.SearchResponse(
        total=len(reports),
        items=reports,
    )

@app.get("/api/search/matches/{report_id}", response_model=schemas.SearchResponse)
def search_matches(
    report_id: int,
    db: Session = Depends(get_db),
):
    target, reports = crud.find_matches_for_report(db, report_id=report_id)

    if target is None:
        # anggap saja 'tidak ada match'
        return schemas.SearchResponse(total=0, items=[])

    return schemas.SearchResponse(
        total=len(reports),
        items=reports,
    )
