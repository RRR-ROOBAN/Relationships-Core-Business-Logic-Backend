from pydantic import BaseModel
from typing import List
from datetime import datetime
from pydantic import validator
from datetime import datetime

# 🧾 Item Create
class InvoiceItemCreate(BaseModel):
    product_name: str
    quantity: int
    price: float


# 🧾 Invoice Create
class InvoiceCreate(BaseModel):
    customer_id: int
    tax: float = 0
    discount: float = 0
    due_date: datetime
    items: List[InvoiceItemCreate]
    
    @validator("due_date")
    def due_date_must_be_future(cls, v):
        if v <= datetime.utcnow():
            raise ValueError("Due date must be in the future")
        return v


# 📦 Item Response
class InvoiceItemResponse(BaseModel):
    product_name: str
    quantity: int
    price: float

    class Config:
        from_attributes = True
        
    @validator("quantity", "price")
    def must_be_positive(cls, v):
        if v <= 0:
            raise ValueError("Must be greater than 0")
        return v


# 🧾 Invoice Response
class InvoiceResponse(BaseModel):
    id: int
    customer_id: int
    tax: float
    discount: float
    due_date: datetime
    total_amount: float
    status: str
    items: List[InvoiceItemResponse]

    class Config:
        from_attributes = True