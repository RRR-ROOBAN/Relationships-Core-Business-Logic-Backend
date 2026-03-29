from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional, List
from datetime import datetime

from database import SessionLocal
from schemas.invoice import InvoiceCreate, InvoiceResponse
from services import invoice_service
from models.invoice import Invoice
from core.dependencies import get_current_user
from models.user import User

router = APIRouter()


# 🔹 DB Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# 🟢 CREATE INVOICE (Protected)
@router.post("/", response_model=InvoiceResponse)
def create_invoice(
    invoice: InvoiceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        return invoice_service.create_invoice(db, invoice)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# 🟢 GET ALL INVOICES (FILTERING)
@router.get("/", response_model=dict)
def get_all_invoices(
    status: Optional[str] = Query(None),
    due_date_before: Optional[datetime] = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(5, ge=1),
    db: Session = Depends(get_db)
):
    query = db.query(Invoice)

    # 🔹 filtering
    if status:
        query = query.filter(Invoice.status == status)

    if due_date_before:
        query = query.filter(Invoice.due_date < due_date_before)

    # 🔹 total count
    total = query.count()

    # 🔹 pagination logic
    skip = (page - 1) * limit

    invoices = query.offset(skip).limit(limit).all()

    data = [InvoiceResponse.from_orm(inv) for inv in invoices]
    
    return {
        "total": total,
        "page": page,
        "limit": limit,
        "data": data
    }


# 🟢 GET CUSTOMER INVOICES
@router.get("/customer/{customer_id}", response_model=List[InvoiceResponse])
def get_customer_invoices(customer_id: int, db: Session = Depends(get_db)):
    invoices = db.query(Invoice).filter(Invoice.customer_id == customer_id).all()

    if not invoices:
        raise HTTPException(status_code=404, detail="No invoices found for this customer")

    return invoices


# 🟢 GET INVOICE SUMMARY
@router.get("/{invoice_id}/summary")
def get_invoice_summary(invoice_id: int, db: Session = Depends(get_db)):
    invoice = db.query(Invoice).filter(Invoice.id == invoice_id).first()

    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")

    total_paid = sum(p.amount for p in invoice.payments) if invoice.payments else 0
    balance = invoice.total_amount - total_paid

    from datetime import datetime

    # 🔥 clean overdue logic
    due = invoice.due_date

    if due is not None and due < datetime.utcnow() and invoice.status != "PAID":  # type: ignore
        invoice.status = "OVERDUE"
        db.commit()

    return {
        "invoice_id": invoice.id,
        "total_amount": invoice.total_amount,
        "total_paid": total_paid,
        "balance": balance,
        "status": invoice.status
    }

# 🟢 GET SINGLE INVOICE (KEEP LAST )
@router.get("/{invoice_id}", response_model=InvoiceResponse)
def get_invoice(invoice_id: int, db: Session = Depends(get_db)):
    invoice = db.query(Invoice).filter(Invoice.id == invoice_id).first()

    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")

    return invoice