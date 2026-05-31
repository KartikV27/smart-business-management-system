from pydantic import BaseModel
from typing import List
from datetime import datetime

class SaleItemBase(BaseModel):
    product_id: int
    quantity: int

class SaleItemCreate(SaleItemBase):
    pass

class SaleItemResponse(SaleItemBase):
    id: int
    sale_id: int
    price: float # Captured at the time of sale

    class Config:
        from_attributes = True

class SaleBase(BaseModel):
    customer_id: int

class SaleCreate(SaleBase):
    items: List[SaleItemCreate]

class SaleResponse(SaleBase):
    id: int
    sale_date: datetime
    total_amount: float
    items: List[SaleItemResponse]

    class Config:
        from_attributes = True
