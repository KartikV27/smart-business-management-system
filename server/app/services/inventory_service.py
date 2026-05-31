from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.product_model import Product
from typing import List

def get_low_stock_products(db: Session, threshold: int = 5) -> List[Product]:
    """
    Returns products with stock equal to or below the given threshold.
    """
    return db.query(Product).filter(Product.stock <= threshold).all()

def adjust_stock(db: Session, product_id: int, quantity_change: int) -> Product:
    """
    Manually adjusts stock (positive for restock, negative for shrinkage/loss).
    Throws an error if the resulting stock is less than 0.
    """
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with ID {product_id} not found"
        )
    
    if product.stock + quantity_change < 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot adjust stock. Product {product.name} only has {product.stock} items available."
        )
    
    product.stock += quantity_change
    db.commit()
    db.refresh(product)
    return product
