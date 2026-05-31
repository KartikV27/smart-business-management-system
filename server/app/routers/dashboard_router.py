from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.connection import SessionLocal
from app.schemas.dashboard_schema import DashboardSummary
from app.services.dashboard_service import get_dashboard_summary

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/dashboard/summary", response_model=DashboardSummary)
def read_dashboard_summary(db: Session = Depends(get_db)):
    """
    Fetch aggregated business health metrics for the dashboard UI.
    """
    return get_dashboard_summary(db)
