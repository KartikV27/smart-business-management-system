from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.product_model import Product
from app.models.customer_model import Customer
from app.models.sale_model import Sale
from app.schemas.dashboard_schema import DashboardSummary

def get_dashboard_summary(db: Session) -> DashboardSummary:
    """
    Executes fast aggregate SQL queries to determine key performance indicators.
    """
    total_revenue = db.query(func.sum(Sale.total_amount)).scalar() or 0.0
    total_customers = db.query(func.count(Customer.id)).scalar() or 0
    total_products = db.query(func.count(Product.id)).scalar() or 0
    total_sales = db.query(func.count(Sale.id)).scalar() or 0
    low_stock_alerts = db.query(func.count(Product.id)).filter(Product.stock <= 5).scalar() or 0

    return DashboardSummary(
        total_revenue=total_revenue,
        total_customers=total_customers,
        total_products=total_products,
        total_sales=total_sales,
        low_stock_alerts=low_stock_alerts
    )
