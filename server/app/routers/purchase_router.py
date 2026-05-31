from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database.connection import SessionLocal
from app.models.purchase_model import Purchase, PurchaseItem, Vendor
from app.models.product_model import Product
from app.schemas.purchase_schema import PurchaseCreate, PurchaseResponse, VendorCreate, VendorResponse

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- VENDORS ---
@router.post("/vendors", response_model=VendorResponse, status_code=status.HTTP_201_CREATED)
def create_vendor(vendor: VendorCreate, db: Session = Depends(get_db)):
    new_vendor = Vendor(**vendor.model_dump())
    db.add(new_vendor)
    db.commit()
    db.refresh(new_vendor)
    return new_vendor

@router.get("/vendors", response_model=List[VendorResponse])
def get_vendors(db: Session = Depends(get_db)):
    return db.query(Vendor).all()

# --- PURCHASES (Inbound Restocking) ---
@router.post("/purchases", response_model=PurchaseResponse, status_code=status.HTTP_201_CREATED)
def create_purchase(purchase_data: PurchaseCreate, db: Session = Depends(get_db)):
    """
    Atomically processes a purchase transaction:
    1. Validates the vendor exists.
    2. Calculates total cost.
    3. Adds stock to products automatically.
    4. Records the purchase.
    """
    vendor = db.query(Vendor).filter(Vendor.id == purchase_data.vendor_id).first()
    if not vendor:
        raise HTTPException(status_code=404, detail="Vendor not found")

    if not purchase_data.items:
        raise HTTPException(status_code=400, detail="Purchase must contain at least one item")

    try:
        new_purchase = Purchase(vendor_id=vendor.id, total_cost=0.0)
        db.add(new_purchase)
        db.flush() # Get new_purchase.id

        total_cost = 0.0

        for item_data in purchase_data.items:
            product = db.query(Product).with_for_update().filter(Product.id == item_data.product_id).first()
            if not product:
                raise HTTPException(status_code=404, detail=f"Product with ID {item_data.product_id} not found")
            
            # Calculate cost and ADD to stock
            item_total = item_data.unit_cost * item_data.quantity
            total_cost += item_total
            product.stock += item_data.quantity

            purchase_item = PurchaseItem(
                purchase_id=new_purchase.id,
                product_id=product.id,
                quantity=item_data.quantity,
                unit_cost=item_data.unit_cost
            )
            db.add(purchase_item)

        new_purchase.total_cost = total_cost
        db.commit()
        db.refresh(new_purchase)
        return new_purchase

    except Exception as e:
        db.rollback()
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/purchases", response_model=List[PurchaseResponse])
def get_purchases(db: Session = Depends(get_db)):
    return db.query(Purchase).all()
