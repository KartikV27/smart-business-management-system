from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database.connection import SessionLocal
from app.models.customer_model import Customer
from app.schemas.customer_schema import CustomerCreate, CustomerResponse

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/customers", response_model=List[CustomerResponse])
def get_customers(db: Session = Depends(get_db)):
    return db.query(Customer).all()

@router.get("/customers/{id}", response_model=CustomerResponse)
def get_customer(id: int, db: Session = Depends(get_db)):
    customer = db.query(Customer).filter(Customer.id == id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer

@router.post("/customers", response_model=CustomerResponse, status_code=status.HTTP_201_CREATED)
def create_customer(customer: CustomerCreate, db: Session = Depends(get_db)):
    new_customer = Customer(
        name=customer.name,
        phone=customer.phone,
        email=customer.email,
        address=customer.address
    )
    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)
    return new_customer

@router.put("/customers/{id}", response_model=CustomerResponse)
def update_customer(id: int, customer_update: CustomerCreate, db: Session = Depends(get_db)):
    db_customer = db.query(Customer).filter(Customer.id == id).first()
    if not db_customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    db_customer.name = customer_update.name
    db_customer.phone = customer_update.phone
    db_customer.email = customer_update.email
    db_customer.address = customer_update.address

    db.commit()
    db.refresh(db_customer)
    return db_customer
