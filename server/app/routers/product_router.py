from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database.connection import SessionLocal
from app.models.product_model import Product
from app.schemas.product_schema import ProductCreate, ProductResponse

router = APIRouter()

# Database Session Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


from app.services.inventory_service import get_low_stock_products, adjust_stock

# SEARCH PRODUCTS (Define search BEFORE {id} route to avoid route conflict)
@router.get("/products/search", response_model=List[ProductResponse])
def search_products(q: str, db: Session = Depends(get_db)):
    """
    Search products by name keyword (case-insensitive substring search).
    """
    if not q:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Search query parameter 'q' is required"
        )
    
    products = db.query(Product).filter(Product.name.like(f"%{q}%")).all()
    return products

# LOW STOCK ALERTS
@router.get("/products/low-stock", response_model=List[ProductResponse])
def low_stock_products(threshold: int = 5, db: Session = Depends(get_db)):
    """
    Fetch products whose stock is at or below the threshold.
    """
    return get_low_stock_products(db, threshold)

# ADJUST STOCK
@router.patch("/products/{id}/stock", response_model=ProductResponse)
def adjust_product_stock(id: int, quantity_change: int, db: Session = Depends(get_db)):
    """
    Manually adjust product stock (e.g. restock or shrinkage).
    """
    return adjust_stock(db, id, quantity_change)

# GET ALL PRODUCTS
@router.get("/products", response_model=List[ProductResponse])
def get_products(db: Session = Depends(get_db)):
    """
    Fetch all products.
    """
    products = db.query(Product).all()
    return products


# GET PRODUCT BY ID
@router.get("/products/{id}", response_model=ProductResponse)
def get_product(id: int, db: Session = Depends(get_db)):
    """
    Fetch a single product by its unique ID.
    """
    product = db.query(Product).filter(Product.id == id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with ID {id} not found"
        )
    return product


# ADD PRODUCT
@router.post("/products", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def add_product(product: ProductCreate, db: Session = Depends(get_db)):
    """
    Create a new product.
    """
    new_product = Product(
        name=product.name,
        price=product.price,
        stock=product.stock
    )

    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product


# UPDATE PRODUCT
@router.put("/products/{id}", response_model=ProductResponse)
def update_product(id: int, product_update: ProductCreate, db: Session = Depends(get_db)):
    """
    Update details of an existing product.
    """
    db_product = db.query(Product).filter(Product.id == id).first()
    if not db_product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with ID {id} not found"
        )
    
    db_product.name = product_update.name
    db_product.price = product_update.price
    db_product.stock = product_update.stock

    db.commit()
    db.refresh(db_product)
    return db_product


# DELETE PRODUCT
@router.delete("/products/{id}", status_code=status.HTTP_200_OK)
def delete_product(id: int, db: Session = Depends(get_db)):
    """
    Delete a product by its ID.
    """
    db_product = db.query(Product).filter(Product.id == id).first()
    if not db_product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with ID {id} not found"
        )
    
    db.delete(db_product)
    db.commit()
    return {"message": "Product Deleted Successfully"}