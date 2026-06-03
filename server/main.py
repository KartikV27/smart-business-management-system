from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers.product_router import router as product_router
from app.routers.customer_router import router as customer_router
from app.routers.sale_router import router as sale_router
from app.routers.dashboard_router import router as dashboard_router
from app.routers.purchase_router import router as purchase_router
from app.database.connection import engine, Base

# Import all models here so Base knows about them before create_all
import app.models.product_model
import app.models.customer_model
import app.models.sale_model
import app.models.purchase_model

app = FastAPI()

# Enable CORS for Angular frontend (running on port 4200)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create Tables
Base.metadata.create_all(bind=engine)

@app.get("/")
def home():
    return {"message": "Smart Business Management Backend Running"}

from fastapi import Depends
from app.core.security import get_current_user_payload

# Include Routers with JWT Security Dependency
app.include_router(dashboard_router, tags=["Dashboard"], dependencies=[Depends(get_current_user_payload)])
app.include_router(product_router, tags=["Products"], dependencies=[Depends(get_current_user_payload)])
app.include_router(purchase_router, tags=["Purchases"], dependencies=[Depends(get_current_user_payload)])
app.include_router(sale_router, tags=["Sales/Billing"], dependencies=[Depends(get_current_user_payload)])
app.include_router(customer_router, tags=["Customers"], dependencies=[Depends(get_current_user_payload)])