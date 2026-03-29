from models.payment import Payment
from models.invoice import Invoice

def create_payment(db, invoice_id, payment_data):

    invoice = db.query(Invoice).filter(Invoice.id == invoice_id).first()

    if not invoice:
        raise ValueError("Invoice not found")

    # 🔹 total paid so far
    total_paid = sum(p.amount for p in invoice.payments)

    # 🔹 prevent overpayment
    if total_paid + payment_data.amount > invoice.total_amount:
        raise ValueError("Payment exceeds invoice amount")
    
    
    # ❌ prevent already paid
    if invoice.status == "PAID":
        raise ValueError("Invoice already fully paid")

    # ❌ duplicate payment
    for p in invoice.payments:
        if p.amount == payment_data.amount:
            raise ValueError("Duplicate payment detected")

    # ❌ overpayment
    if total_paid + payment_data.amount > invoice.total_amount:
        raise ValueError("Payment exceeds invoice amount")

    # 🔹 create payment
    payment = Payment(
        amount=payment_data.amount,
        payment_method=payment_data.payment_method,
        status="SUCCESS",
        invoice_id=invoice_id
    )

    db.add(payment)
    db.commit()
    db.refresh(payment)

    # 🔹 update invoice status
    total_paid += payment_data.amount

    if total_paid == invoice.total_amount:
        invoice.status = "PAID"
    else:
        invoice.status = "PARTIAL"

    db.commit()

    return payment