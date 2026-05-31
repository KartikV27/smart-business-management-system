from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from app.database.connection import SessionLocal
from app.models.sale_model import Sale
from app.schemas.sale_schema import SaleCreate, SaleResponse
from app.services.sales_service import process_sale

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/sales", response_model=SaleResponse, status_code=status.HTTP_201_CREATED)
def create_sale(sale: SaleCreate, db: Session = Depends(get_db)):
    """
    Creates a new sale atomically. Deducts inventory and sets historical prices.
    """
    return process_sale(db, sale)

@router.get("/sales", response_model=List[SaleResponse])
def get_sales(db: Session = Depends(get_db)):
    """
    Fetch all historical sales.
    """
    return db.query(Sale).all()
