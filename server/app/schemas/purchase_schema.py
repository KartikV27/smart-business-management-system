from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# --- Vendor Schemas ---
class VendorBase(BaseModel):
    name: str
    contact_email: Optional[str] = None
    contact_phone: Optional[str] = None

class VendorCreate(VendorBase):
    pass

class VendorResponse(VendorBase):
    id: int

    class Config:
        from_attributes = True

# --- Purchase Schemas ---
class PurchaseItemBase(BaseModel):
    product_id: int
    quantity: int
    unit_cost: float

class PurchaseItemCreate(PurchaseItemBase):
    pass

class PurchaseItemResponse(PurchaseItemBase):
    id: int
    purchase_id: int

    class Config:
        from_attributes = True

class PurchaseBase(BaseModel):
    vendor_id: int

class PurchaseCreate(PurchaseBase):
    items: List[PurchaseItemCreate]

class PurchaseResponse(PurchaseBase):
    id: int
    purchase_date: datetime
    total_cost: float
    items: List[PurchaseItemResponse]

    class Config:
        from_attributes = True
