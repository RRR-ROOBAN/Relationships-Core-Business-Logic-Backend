from pydantic import BaseModel, validator
from enum import Enum


class PaymentMethod(str, Enum):
    UPI = "UPI"
    CARD = "CARD"
    WALLET = "WALLET"


class PaymentCreate(BaseModel):
    amount: float
    payment_method: PaymentMethod

    @validator("amount")
    def amount_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError("Amount must be greater than 0")
        return v


class PaymentResponse(BaseModel):
    id: int
    amount: float
    payment_method: str
    status: str
    invoice_id: int

    class Config:
        from_attributes = True   # or orm_mode = True