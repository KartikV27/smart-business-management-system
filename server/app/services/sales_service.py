from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.product_model import Product
from app.models.customer_model import Customer
from app.models.sale_model import Sale, SaleItem
from app.schemas.sale_schema import SaleCreate

def process_sale(db: Session, sale_data: SaleCreate) -> Sale:
    """
    Atomically processes a sale transaction:
    1. Validates the customer exists.
    2. Validates product inventory.
    3. Calculates total amount based on current prices.
    4. Deducts stock from products.
    5. Records the sale and sale items.
    Rolls back automatically on failure.
    """
    # 1. Validate Customer
    customer = db.query(Customer).filter(Customer.id == sale_data.customer_id).first()
    if not customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")

    if not sale_data.items:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Sale must contain at least one item")

    try:
        new_sale = Sale(customer_id=customer.id, total_amount=0.0)
        db.add(new_sale)
        db.flush() # Get the new_sale.id without committing

        total_amount = 0.0

        for item_data in sale_data.items:
            # 2. Validate Product Inventory
            product = db.query(Product).with_for_update().filter(Product.id == item_data.product_id).first()
            if not product:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Product with ID {item_data.product_id} not found"
                )
            
            if product.stock < item_data.quantity:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Insufficient stock for {product.name}. Requested: {item_data.quantity}, Available: {product.stock}"
                )

            # 3 & 4. Calculate total and deduct stock
            item_total = product.price * item_data.quantity
            total_amount += item_total
            product.stock -= item_data.quantity

            # 5. Record SaleItem using the current historical price
            sale_item = SaleItem(
                sale_id=new_sale.id,
                product_id=product.id,
                quantity=item_data.quantity,
                price=product.price
            )
            db.add(sale_item)

        # Update the sale total
        new_sale.total_amount = total_amount

        # Commit everything as one atomic transaction
        db.commit()
        db.refresh(new_sale)
        return new_sale

    except Exception as e:
        db.rollback()
        # Re-raise HTTP exceptions, otherwise wrap in a 500 error
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
