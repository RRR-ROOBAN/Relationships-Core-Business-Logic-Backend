from sqlalchemy import Column, Integer, Float, ForeignKey,String
from sqlalchemy.orm import relationship
from database import Base
from sqlalchemy import DateTime
from datetime import datetime


from sqlalchemy import Column, Integer, Float, ForeignKey, String, DateTime
from sqlalchemy.orm import relationship
from database import Base

class Invoice(Base):
    __tablename__ = "invoices"

    id = Column(Integer, primary_key=True, index=True)

    customer_id = Column(Integer, ForeignKey("customers.id"))

    tax = Column(Float, default=0)
    discount = Column(Float, default=0)
    due_date = Column(DateTime)
    total_amount = Column(Float, default=0)


    status = Column(String, default="PENDING")

    # relationships
    items = relationship("InvoiceItem", back_populates="invoice")
    customer = relationship("Customer", back_populates="invoices")
    payments = relationship("Payment", back_populates="invoice")
    
    