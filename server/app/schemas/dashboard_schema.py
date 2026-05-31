from pydantic import BaseModel

class DashboardSummary(BaseModel):
    total_revenue: float
    total_customers: int
    total_products: int
    total_sales: int
    low_stock_alerts: int
