from sqlalchemy import Column, Integer, String
from app.database.connection import Base
from sqlalchemy.orm import relationship

class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    phone = Column(String(20))
    email = Column(String(100))
    address = Column(String(255))

    # Relationship to sales will be linked from the Sale side
    sales = relationship("Sale", back_populates="customer")
