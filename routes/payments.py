from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from schemas.payment import PaymentCreate, PaymentResponse
from services import payment_service
from models.payment import Payment

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# 🔥 MAIN PAYMENT API
@router.post("/pay/{invoice_id}", response_model=PaymentResponse)
def pay_invoice(invoice_id: int, payment: PaymentCreate, db: Session = Depends(get_db)):
    try:
        return payment_service.create_payment(db, invoice_id, payment)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# 🔍 GET payments for invoice
@router.get("/invoice/{invoice_id}")
def get_payments(invoice_id: int, db: Session = Depends(get_db)):
    payments = db.query(Payment).filter(Payment.invoice_id == invoice_id).all()
    return payments

from fastapi import Query
from typing import Optional

@router.get("/", response_model=list[PaymentResponse])
def get_all_payments(
    method: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(Payment)

    if method:
        query = query.filter(Payment.payment_method == method)

    return query.all()