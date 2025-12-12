# app/crud.py
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app import models


def search_reports(
    db: Session,
    keyword: Optional[str] = None,
    location: Optional[str] = None,
    type_: Optional[str] = None,
    status: Optional[str] = None,
    limit: int = 50,
) -> List[models.Report]:
    query = db.query(models.Report)

    if keyword:
        kw = f"%{keyword}%"
        query = query.filter(
            or_(
                models.Report.description.like(kw),
                models.Report.location.like(kw),
            )
        )

    if location:
        query = query.filter(models.Report.location.like(f"%{location}%"))

    if type_:
        query = query.filter(models.Report.type == type_)

    if status:
        query = query.filter(models.Report.status == status)

    query = query.order_by(models.Report.created_at.desc())

    # PENTING: .all() akan mengembalikan [] kalau tidak ada data, BUKAN error
    return query.limit(limit).all()

# app/crud.py

def find_report_by_id(db: Session, report_id: int) -> Optional[models.Report]:
    return db.query(models.Report).filter(models.Report.id == report_id).first()


def find_matches_for_report(
    db: Session,
    report_id: int,
    limit: int = 10,
) -> tuple[Optional[models.Report], list[models.Report]]:
    # 1. Ambil report target
    target = find_report_by_id(db, report_id)
    if target is None:
        # return (target=None, matches=[])
        return None, []

    # 2. Cari report lain dengan lokasi & tipe sama
    q = (
        db.query(models.Report)
        .filter(models.Report.id != target.id)
        .filter(models.Report.type == target.type)
    )

    if target.location:
        q = q.filter(models.Report.location == target.location)

    q = q.order_by(models.Report.created_at.desc())
    matches = q.limit(limit).all()

    return target, matches
